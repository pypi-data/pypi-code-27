from scipy.signal import lfilter

def gen(ir_data, source_data):
    buffer_len = 1024
    #b, a = butter(3, 0.05)
    b, a = ir_data[:buffer_len], [1]

    offset = 1024
    for start in range(buffer_len, len(source_data), buffer_len):
        dataslice = source_data[start-offset:start+buffer_len]
        conv = lfilter(b, a, dataslice)
        yield conv[offset:]
