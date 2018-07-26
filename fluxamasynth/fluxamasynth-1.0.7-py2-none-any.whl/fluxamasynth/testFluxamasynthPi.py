import fluxamasynth
from time import sleep
import random

fluxamasynth.init()

while (1): 
    note = random.randint(0, 127)
    fluxamasynth.noteOn(0, note, 127)
    sleep(float(random.randint(0, 250))/1000)
    fluxamasynth.noteOff(0, note)

