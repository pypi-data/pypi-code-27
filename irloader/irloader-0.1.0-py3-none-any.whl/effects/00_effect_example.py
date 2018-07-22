import numpy

# example of a file_interface function and a stream_interface function

def file_interface(ir_data, source_data):
    ir_vol = numnpy.max(numpy.abs(ir_data))
    src_vol = numnpy.max(numpy.abs(source_data))

    gain = ir_vol / src_vol
    source_data = source_data * gain

    # you can yield the whole result or chunk by chunk
    yield source_data


def stream_interface(ir_data):

    # start by getting source data from a yield.
    source_data = yield None
    assert not source_data is None
    ir_vol = numnpy.max(numpy.abs(ir_data))

    # start a loop and get more data and yield result in same operation:
    #  newdata = yield myresult

    while 1:
        src_vol = numnpy.max(numpy.abs(source_data))
        gain = ir_vol / src_vol
        res = source_data * gain
        source_data = yield res
