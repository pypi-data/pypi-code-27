from .effects import ir_convolve, ir_lfilter
import numpy
from .wavdata import WavData
from .streamaudio import StreamAudio

class IRLoader():
    def __init__(self, ir, source, target, looper=True):
        self.ir = WavData(ir)
        if source:
            self.source = WavData(source)
            self.stream = StreamAudio() if looper else None
        else:
            self.source = None
            self.stream = StreamAudio()
        if target:
            self.target = WavData(target)
        else:
            self.target = None

    def read(self):
        if self.source:
            self.source.read()
            print(self.source.info, self.source.data)

        self.ir.read()
        self.ir.limit()
        print(self.ir.info, self.ir.data)

        if self.source:
            assert self.ir.info == self.source.info
    
    def play(self):
        if self.target:
            assert len(self.target.data) > 1
            assert isinstance(self.target.info, int)
            self.target.play()
        else:
            self.stream.play()
    
    def looper(self):
        self.stream.looper(self.source.data)

    def write(self):
        assert self.target
        self.target.write()

    def process(self):
        if self.source and self.target:
            #target = numpy.concatenate([d for d in ir_lfilter.gen(self.ir.data, self.source.data)])
            target = numpy.concatenate([d for d in ir_convolve.file_interface(self.ir.data, self.source.data)])
            #target = convolve(self.source.data, self.ir.data, mode="same", method="direct")

            # reduce volume before save
            #print(numpy.max(numpy.abs(target)))
            #target = target / numpy.max(numpy.abs(target))
            target = target * 0.5

            self.target.replace(self.source.info, target)

        if self.stream:
            self.stream.setup(self.ir.data, self.ir.info)
