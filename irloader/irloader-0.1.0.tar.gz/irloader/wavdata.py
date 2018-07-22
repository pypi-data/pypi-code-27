import soundfile
import sounddevice
import numpy
import copy

class WavData():
    def __init__(self, filename):
        self.filename = filename
        self.info = None
        self.data = None

    def read(self):
        self.data, self.info = soundfile.read(self.filename, dtype="float32")
        assert self.data.ndim > 0
        if self.data.ndim > 1:
            self.data = self.data[:,0]
        print(self.filename, self.data.ndim, type(self.data[0]))
        assert isinstance(self.data[0], numpy.float32)
    
    def play(self, block=True):
            sounddevice.play(self.data, self.info)
            if block:
                sounddevice.wait()


    def replace(self, info, data):
        self.info, self.data = info, copy.copy(data)

    def write(self):
        soundfile.write(
            self.filename,
            self.data,
            self.info,
            subtype="PCM_24"
        )
    
    def boost(self):
        # boost max to 1.0
        self.data =  self.data / numpy.max(numpy.abs(self.data))

    def limit(self):
        # limit to max 0.055. to ensure the convolve result is below 1.0
        maxf = numpy.max(numpy.abs(self.data)) * 18
        self.data =  self.data / maxf
