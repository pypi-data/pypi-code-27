from .irloader import IRLoader
from scipy.signal import convolve, butter
import sounddevice
import numpy
import time
from functools import partial
prev = None
def main():
    irloader = IRLoader(
        #ir="data/Engl412St2a_32bit.wav",
        ir="data/Engl412St2b_32bit.wav",
        #ir="data/MarshallHeritageG12H2a_32bit.wav",
        #ir="data/TNMar412-V30Blend1_32bit.wav",
        #ir="data/Engl412St2b_32bit_441.wav",
        source="data/src.wav",
        target="data/target.wav")

    irloader.read()
    #irloader.process()
    #irloader.write()
    #irloader.play()
    #print("done")

    sd = sounddevice
    sd.default.samplerate = irloader.ir.info
    sd.default.channels = 1, 1

    offset = 416
    irslice = irloader.ir.data[:offset]
    global prev
    prev = numpy.array([0] * offset)

    def Loopy():
        source_data = irloader.source.data
        while 1:
            for start in range(0, len(source_data), offset):
                dataslice = source_data[start:start + offset]
                try:
                    dataslice = dataslice.reshape((offset, 1))
                except ValueError:
                    break
                yield dataslice
    
    loopy = Loopy()

    def callback(indata, outdata, frames, time_, status):
        global prev
        if numpy.max(prev) == 0:
            print (frames)
            print(sd.default.samplerate)
        if status:
            print(status)
        #indata = next(loopy)
        sig = indata[:,0]
        sig = sig * 3
        res = numpy.concatenate([prev, sig])
        prev = sig[-offset:]
        res = convolve(res, irslice, mode="full", method="direct")
        res = res[offset:offset+frames]
        if numpy.max(numpy.abs(res)) > 0.9:
            print("HIGH")
        outdata[:,0] = res
    
    try:
        with sd.Stream(channels=1, latency=0.03, dtype='float32', callback=callback):
            while 1:
                time.sleep(1000)
    except KeyboardInterrupt:
        pass
