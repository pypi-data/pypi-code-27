import glob
import os
import types

import zipstream
from zipfile import ZIP_DEFLATED


class IterStreamer(object):
    """
    Allows file-like read operations (read, seek, tell) on iterator contents. Seek and tell are subject to buffer size.
    """
    def __init__(self, iterable, buffer_size=2 ** 20):
        """
        Initialize.

        :param iterable: the iterable object to be streamed
        :param buffer_size: a guideline length for the internal buffer. The buffer is of dynamic length, and buffer_size
        is used only for guiding the trimming. The Buffer is expanded by consuming from the iterable. It is trimmed to
        buffer_size/2 when length of the portion of the buffer before current position exceeds buffer_size/2. Trimming
        is invoked by read().

        """
        self._buffer_size = buffer_size
        self._iterable = iter(iterable)
        self._global_position = 0
        self._position_in_buffer = 0
        self._buffer = ''
        self._end_of_iterator = False

    def _trim_buffer(self):
        # see comment on parameter buffer_size of __init__ above
        if self._position_in_buffer > self._buffer_size/2:
            new_start = self._position_in_buffer - self._buffer_size/2
            self._buffer = self._buffer[new_start:]
            self._position_in_buffer -= new_start

    def read(self, size):
        length_to_return = (len(self._buffer) - self._position_in_buffer)
        try:
            while (len(self._buffer) - self._position_in_buffer) < size:
                data = next(self._iterable)
                length_to_return += len(data)
                self._buffer += data
        except StopIteration:
            # actually read read_data_length
            size = length_to_return
        self._trim_buffer()
        # advance the position pointers
        self._position_in_buffer += size
        self._global_position += size
        # since the pointers have been advanced, start and end indices of return value are computed relative to the new
        # position_in_buffer
        return self._buffer[self._position_in_buffer-size:self._position_in_buffer]

    def seek(self, offset, from_what=0):
        if from_what != 0 and from_what != 1:
            raise IOError('Offsets from end are not supported')
        elif from_what == 0:
            self.seek(offset-self._global_position, 1)
        else:
            new_position = self._position_in_buffer+offset
            if new_position < 0 or new_position > len(self._buffer):
                raise IOError('Cannot fast-forward/rewind outside current buffer.')
            self._position_in_buffer = new_position
            self._global_position += offset

    def tell(self):
        return self._global_position


class StreamingArchive(object):
    def __init__(self, input_data, archive_name, compress_type=ZIP_DEFLATED, progress_callback=None):
        """
        StreamingArchive can be used for streaming compression of input_data contents using a file-like stream.

        :param input_data: data to compress. Can be a list of filepaths, a string holding a valid path to either a file
            or a directory, an iterable, or a list of iterables.
        :param archive_name: name for the root directory.
        :param compress_type: either zipfile.ZIP_DEFLATED (compressed with deflate algorithm) or zipfile.ZIP_STORED
            (uncompressed)
        :param progress_callback: optional callback which will be called every ~500kb with a percentage progress.
            This only works properly if all items being compressed are files, not iterables.
        """
        self._progress_callback = progress_callback
        self._zipfile = zipstream.ZipFile(allowZip64=True)
        # if the installed version of zipstream includes the progress bar customization, use it. Otherwise, report 50%
        if hasattr(self._zipfile, 'get_progress'):
            self._zipfile_progress = self._zipfile.get_progress
        else:
            self._zipfile_progress = lambda: 0.5

        def iterable_item_and_arcname(itr):
            return itr, '{0}{1}iterable_{2}'.format(archive_name, os.sep, itr.__hash__())

        if isinstance(input_data, str) or isinstance(input_data, unicode):
            # a string input_data needs to be a valid file or directory
            if not os.path.exists(input_data) or (not os.path.isfile(input_data) and not os.path.isdir(input_data)):
                raise IOError(
                        "Invalid input parameter input_files: {0} is a string but not a valid file/directory path".format(input_data)
                    )
            if os.path.isfile(input_data):
                # items needs to be a list, make a list of one element
                items = [(
                    input_data,
                    '{0}{1}{2}'.format(archive_name, os.sep, os.path.basename(input_data))
                )]
            else:
                # this is a directory. compress all files in the directory.
                items = []
                for root, _, files in os.walk(input_data):
                    for name in files:
                        fpath = root + os.sep + name
                        # for arcname, use path relative to the root directory (passed as input_data)
                        items.append((
                            fpath,
                            '{0}{1}{2}'.format(archive_name, os.sep, os.path.relpath(fpath, start=input_data))
                        ))
        elif isinstance(input_data, types.GeneratorType):
            # items needs to be a list, make a list of one element
            items = [(iterable_item_and_arcname(input_data))]
        elif isinstance(input_data, list):
            # every element in a list needs to be an iterable or a valid file path
            items = []
            for item in input_data:
                if isinstance(item, types.GeneratorType):
                    items.append((iterable_item_and_arcname(item)))
                elif isinstance(item, str) or isinstance(item, unicode):
                    if not os.path.exists(item) or not os.path.isfile(item):
                        raise IOError(
                            "Invalid input list element: {0} is a string but not a valid file path".format(item)
                        )
                    items.append((
                        item,
                        '{0}{1}{2}'.format(archive_name, os.sep, os.path.basename(item))
                    ))
        else:
            raise RuntimeError('input_date has invalid type: must be one of (str, unicode, types.GeneratorType, list)')

        for item, arcname in items:
            if isinstance(item, types.GeneratorType):
                self._zipfile.write_iter(arcname=arcname, iterable=item, compress_type=compress_type)
            elif os.path.exists(item) and os.path.isfile(item):
                self._zipfile.write(filename=item, arcname=arcname, compress_type=compress_type)
            else:
                raise IOError("Invalid list or generator element: {0}. Input_paths == {1}".format(item, input_data))

    def get_progress(self):
        """
        Get percentage of uncompressed data that has already been processed.
        This only works properly if all items being compressed are files, not iterables.
        """
        return self._zipfile_progress()

    def get_compressed_stream(self):
        """
        Get a file-like stream of compressed data
        :return:
        """
        if self._progress_callback and callable(self._progress_callback):
            def report_progress(itr):
                for index, item in enumerate(itr):
                    # zipstream library reads files in 8192 byte increments. This is too fine-grained,
                    # so report progress for every ~500kb
                    if index % 2**6 == 0:
                        self._progress_callback(self._zipfile_progress())
                    yield item
                self._progress_callback(self._zipfile_progress())
            iterable = report_progress(self._zipfile)
        else:
            iterable = self._zipfile
        return IterStreamer(iterable)
