import numpy

def _test_reference(ir_data, source_data):
    buffer_len = 1024
    irslice = ir_data[:buffer_len]
    offset = 1024
    for start in range(buffer_len, len(source_data), buffer_len):
        dataslice = source_data[start - offset:start + buffer_len]
        conv = numpy.convolve(dataslice, irslice, mode="full")
        yield conv[offset:offset + buffer_len]


def file_interface(ir_data, source_data):
    loop = stream_interface(ir_data)
    loop.send(None)
    for start in range(0, len(source_data), 1024):
        res = loop.send(source_data[start:start + 1024])
        yield res

def stream_interface(ir_data):
    source_data = yield None
    assert not source_data is None

    prev_data = None
    offset = len(source_data)

    irslice = ir_data[:1024]

    #init signal
    signal = numpy.concatenate([source_data, source_data])

    while 1:
        conv = numpy.convolve(signal, irslice, mode="full")
        res = conv[offset:offset + len(source_data)]

        prev_data = source_data
        offset = len(prev_data)

        source_data = yield res

        signal = numpy.concatenate([prev_data, source_data])
