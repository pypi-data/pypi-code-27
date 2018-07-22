import sounddevice
from .effects import ir_convolve
import numpy

class StreamAudio():
    def __init__(self):
        self.info = sounddevice.default.samplerate
        sounddevice.default.channels = 1, 1
    
    def setup(self, ir_data, ir_samplerate):
        self.info = ir_samplerate
        sounddevice.default.samplerate = self.info
        self.ir_data = ir_data

    def play(self):
        convolve_interface = ir_convolve.stream_interface(self.ir_data)
        convolve_interface.send(None)

        def callback(indata, outdata, frames, time_, status):
            if status:
                print(status)
            #indata = next(loopy)
            sig = indata[:,0]
            sig = sig * 3
            res = convolve_interface.send(sig)
            if numpy.max(numpy.abs(res)) > 0.9:
                print("HIGH")
            outdata[:,0] = res

        try:
            with sounddevice.Stream(channels=1, latency=0.03, dtype='float32', callback=callback):
                while 1:
                    sounddevice.sleep(1000)
        except KeyboardInterrupt:
            pass


    def looper(self, source_data):
        offset = 1024
        def Loopy():
            while 1:
                for start in range(0, len(source_data), offset):
                    dataslice = source_data[start:start + offset]
                    if len(dataslice) == offset:
                        yield dataslice
    
        loopy = Loopy()

        convolve_interface = ir_convolve.stream_interface(self.ir_data)
        convolve_interface.send(None)

        def callback(indata, outdata, frames, time_, status):
            if status:
                print(status)
            sig = next(loopy)
            res = convolve_interface.send(sig)
            if numpy.max(numpy.abs(res)) > 0.9:
                print("HIGH")
            outdata[:,0] = res

        try:
            with sounddevice.Stream(channels=1, blocksize=1024, latency=0.1, dtype='float32', callback=callback):
                while 1:
                    sounddevice.sleep(1000)
        except KeyboardInterrupt:
            pass
