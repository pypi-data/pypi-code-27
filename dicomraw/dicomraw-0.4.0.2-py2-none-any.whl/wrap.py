from struct import unpack

from pydicom.dataelem import DataElement
from pydicom.filebase import DicomBytesIO
from pydicom.filereader import read_partial, read_sequence_item
from pydicom.filewriter import write_sequence_item, write_dataset
from pydicom.sequence import Sequence
from pydicom.tag import SequenceDelimiterTag, Tag

from pydicom.dataset import Dataset
from pydicom.charset import default_encoding


def encode(ds, is_implicit_vr, is_little_endian, is_sequence_item=False):
    """Encode a pydicom Dataset `ds` to a byte stream.
    (from https://github.com/pydicom/pynetdicom3)
    Parameters
    ----------
    ds : pydicom.dataset.Dataset
        The dataset to encode
    is_implicit_vr : bool
        The element encoding scheme the dataset will be encoded with.
    is_little_endian : bool
        The byte ordering the dataset will be encoded in.
    is_sequence_item: bool
        Set to true to write a sequence item

    Returns
    -------
    bytes or None
        The encoded dataset (if successful)
    """
    # pylint: disable=broad-except
    fp = DicomBytesIO()
    fp.is_implicit_VR = is_implicit_vr
    fp.is_little_endian = is_little_endian
    try:
        if is_sequence_item:
            write_sequence_item(fp, ds, default_encoding)
        else:
            write_dataset(fp, ds)
    except Exception:
        fp.close()
        raise

    bytestring = fp.parent.getvalue()
    fp.close()

    return bytestring


class RawWrapper(object):

    def __init__(self, input_stream, wrapped_content_tag, is_implicit_vr=False, is_little_endian=True, buffer_size=2**20):
        self._input_stream = input_stream
        self._is_implicit_vr = is_implicit_vr
        self._is_little_endian = is_little_endian
        self._buffer_size = buffer_size
        if buffer_size % 2 == 1:
            raise RuntimeError("DICOM standard mandates even-sized value length, so buffer_size must be even.")
        dataset = Dataset()
        dataset[wrapped_content_tag] = DataElement(wrapped_content_tag, "SQ", Sequence(), is_undefined_length=True)
        encoded = encode(dataset, is_implicit_vr=is_implicit_vr, is_little_endian=is_little_endian)

        # a low-level method of splitting the empty dataset into prefix
        # (DicomWrapperCreator element and DicomWrapperContent SQ element header) and suffix (end of sequence delimiter)
        length_of_sequence_delimiter = 8
        self._prefix = encoded[:-length_of_sequence_delimiter]
        self._suffix = encoded[-length_of_sequence_delimiter:]

    def _encapsulate(self, input_data):
        first_sequence_element = self._prefix is not None

        embedded_ds = Dataset()
        embedded_ds.EncapsulatedDocument = input_data
        encapsulated_sequence_element = encode(
            embedded_ds,
            is_implicit_vr=self._is_implicit_vr,
            is_little_endian=self._is_little_endian,
            is_sequence_item=True
        )

        # prepend prefix is first sequence element
        if first_sequence_element:
            encapsulated_sequence_element = self._prefix + encapsulated_sequence_element
            self._prefix = None
        return encapsulated_sequence_element

    def __iter__(self):

        # cache one data chunk to keep track of which is the last one, in order to append padding byte(s) to it
        input_data = self._input_stream.read(self._buffer_size)
        while True:
            next_data = self._input_stream.read(self._buffer_size)
            incoming_data_length = len(next_data)
            if incoming_data_length == 0:
                # length of next_data is 0, therefore input_data is the last data chunk
                # append padding byte(s)
                if len(input_data) % 2:
                    input_data += "\01"
                else:
                    input_data += "\00\02"
                yield self._encapsulate(input_data)
                yield self._suffix
                return

            yield self._encapsulate(input_data)
            input_data = next_data


class RawUnwrapper(object):

    def __init__(self, input_stream, wrapped_content_tag, is_implicit_vr=False, is_little_endian=True):
        self._is_implicit_vr = is_implicit_vr
        self._is_little_endian = is_little_endian
        self._input_stream = input_stream
        self._wrapped_content_tag = wrapped_content_tag

    def _wrapped_sequence_start(self, tag, *_):
        return tag == self._wrapped_content_tag

    def _endian_format(self):
        if self._is_little_endian:
            return '<'
        else:
            return '>'

    def _end_of_sequence(self):
        # look ahead to next tag and 4 bytes after it
        next_8bytes = self._input_stream.read(8)
        # rewind
        self._input_stream.seek(self._input_stream.tell() - 8)
        next_group, next_element, next_4bytes = unpack(self._endian_format() + "HHL", next_8bytes)

        next_tag = Tag(next_group, next_element)
        return next_tag == SequenceDelimiterTag and next_4bytes == 0

    def __iter__(self):
        # discard dataset elements prior to the wrapped sequence tag
        read_partial(self._input_stream, stop_when=self._wrapped_sequence_start)
        # offset 12 bytes of sequence tag, VR, length in order to advance the buffer to position of first sequence item
        sequence_header_length = 8 if self._is_implicit_vr else 12

        # cache one data chunk to keep track of which is the last one, in order to remove padding byte(s) from it
        self._input_stream.read(sequence_header_length)
        embedded_ds = read_sequence_item(
            self._input_stream, encoding=default_encoding, is_implicit_VR=self._is_implicit_vr,
            is_little_endian=self._is_little_endian)
        while True:
            data = embedded_ds.EncapsulatedDocument
            # explicitly test whether at end of file
            if self._input_stream.read(1) == '':
                next_ds = None
            else:
                self._input_stream.seek(-1, 1)
                next_ds = read_sequence_item(
                    self._input_stream, encoding=default_encoding, is_implicit_VR=self._is_implicit_vr,
                    is_little_endian=self._is_little_endian)

            if next_ds:
                yield data
                embedded_ds = next_ds
            else:
                # remove padding from last data chunk
                num_padding_bytes = ord(data[-1])
                data = data[:-num_padding_bytes]
                yield data
                return


class Wrapper(RawWrapper):

    def __init__(self, input_stream, private_group, content_creator,
                 is_implicit_vr=False, is_little_endian=True, buffer_size=2**20):

        super(Wrapper, self).__init__(input_stream,
                                      wrapped_content_tag=Tag(private_group, 0x1000),
                                      is_implicit_vr=is_implicit_vr,
                                      is_little_endian=is_little_endian,
                                      buffer_size=buffer_size
                                      )
        dataset = Dataset()
        content_creator_tag = Tag(private_group, 0x0010)
        dataset[content_creator_tag] = DataElement(content_creator_tag, "LO", content_creator)
        encoded = encode(dataset, is_implicit_vr=is_implicit_vr, is_little_endian=is_little_endian)
        self._prefix = encoded + self._prefix


class Unwrapper(RawUnwrapper):
    def __init__(self, input_stream, private_group, is_implicit_vr=False, is_little_endian=True):
        super(Unwrapper, self).__init__(input_stream,
                                        wrapped_content_tag=Tag(private_group, 0x1000),
                                        is_implicit_vr=is_implicit_vr,
                                        is_little_endian=is_little_endian)
