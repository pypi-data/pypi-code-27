import serial
port = "/dev/ttyS0"
serialPort = serial.Serial()

def setPort(p):
    port = p
    
def init():
    serialPort.baudrate = 31250
    serialPort.port = port
    serialPort.open()
    serialPort.flushInput

def noteOn(channel, pitch, velocity):
    packet = [ 0x90 | (channel & 0x0f), pitch, velocity];
    serialPort.write(bytearray(packet))


def noteOff(channel, pitch):
    packet = [ 0x80 | (channel & 0x0f), pitch, 0x00 ];
    serialPort.write(bytearray(packet))

def programChange(bank, channel, v): 
    # bank is either 0 or 127
    packet =[ 0xB0 | (channel & 0x0f), byte(0x00), bank];
    serialPort.write(bytearray(packet))
    serialPort.write(bytearray(0xc0 | (channel & 0x0f)))

def pitchBend(channel, v): 
    # v is a value from 0 to 1023
    # it is mapped to the full range 0 to 0x3fff (16383)
    #v = map(v, 0, 1023, 0, 0x3fff);
    v = v * (16383 - 1023) / (1023);
    packet = [  0xe0 | (channel & 0x0f), byte(v & 0x00ef), byte(v >> 7)];
    serialPort.write(bytearray(packet))

def pitchBendRange(channel, v): 
    # Also called pitch bend sensitivity
    #BnH 65H 00H 64H 00H 06H vv
    packet = [ 0xb0 | (channel & 0x0f), 0x65, 0x00, 0x64, 0x00, 0x06, (v & 0x7f)];
    serialPort.write(bytearray(packet))

def midiReset(): 
    serialPort.write(bytearray(0xff))

def setChannelVolume(channel, level): 
    packet = [  (0xb0 | (channel & 0x0f)), 0x07, level];
    serialPort.write(bytearray(packet))

def allNotesOff(channel): 
    # BnH 7BH 00H
    packet = [  (0xb0 | (channel & 0x0f)), 0x7b, 0x00];
    serialPort.write(bytearray(packet))

def setMasterVolume(level): 
    #F0H 7FH 7FH 04H 01H 00H ll F7H
    packet = [  0xf0, 0x7f, 0x7f, 0x04, 0x01, 0x00, (level & 0x7f), 0xf7];
    serialPort.write(bytearray(packet))

def setReverb(channel, program, level, delayFeedback): 
    # Program 
    # 0: Room1   1: Room2    2: Room3 
    # 3: Hall1   4: Hall2    5: Plate
    # 6: Delay   7: Pan delay
    serialPort.write(bytearray(0xb0 | (channel & 0x0f)))
    serialPort.write(bytearray(0x50))
    serialPort.write(bytearray(program & 0x07))
 
    # Set send level
    serialPort.write(bytearray(xb0 | (channel & 0x0f)))
    serialPort.write(bytearray(0x5b))
    serialPort.write(bytearray(level & 0x7f))
  
    if (delayFeedback > 0): 
      #F0H 41H 00H 42H 12H 40H 01H 35H vv xx F7H
      packet = [  0xf0, 0x41, byte(0x00), 0x42, 0x12, 0x40, 0x01, 0x35, (delayFeedback & 0x7f), 0x00, 0xf7];
      serialPort.write(bytearray(packet))
    
def setChorus(channel, program, level, feedback, chorusDelay): 
    # Program 
    # 0: Chorus1   1: Chorus2    2: Chorus3 
    # 3: Chorus4   4: Feedback   5: Flanger
    # 6: Short delay   7: FB delay
    serialPort.write(0xb0 | (channel & 0x0f))
    serialPort.write(0x51)
    serialPort.write(program & 0x07)
 
    # Set send level
    serialPort.write(0xb0 | (channel & 0x0f))
    serialPort.write(0x5d)
    serialPort.write(level & 0x7f)
  
    if (feedback > 0): 
        #F0H 41H 00H 42H 12H 40H 01H 3BH vv xx F7H
	packet = [  0xf0, 0x41, byte(0x00), 0x42, 0x12, 0x40, 0x01, 0x3B, (feedback & 0x7f), 0x00, 0xf7];
	serialPort.write(bytearray(packet))
    
  
    if (chorusDelay > 0): 
        # F0H 41H 00H 42H 12H 40H 01H 3CH vv xx F7H
        packet = [  0xf0, 0x41, byte(0x00), 0x42, 0x12, 0x40, 0x01, 0x3C, (chorusDelay & 0x7f), 0x00, 0xf7];
	serialPort.write(bytearray(packet))

def pan(channel, value): 
    packet = [ (0xb0 | (channel & 0x0f)), 0x0A, (value)  ];
    serialPort.write(bytearray(packet))

def setEQ(channel, lowBand, medLowBand, medHighBand, highBand,
           lowFreq, medLowFreq, medHighFreq, highFreq): 
    #BnH 63H 37H 62H 00H 06H vv   low band
    #BnH 63H 37H 62H 01H 06H vv   medium low band
    #BnH 63H 37H 62H 02H 06H vv   medium high band
    #BnH 63H 37H 62H 03H 06H vv   high band
    #BnH 63H 37H 62H 08H 06H vv   low freq
    #BnH 63H 37H 62H 09H 06H vv   medium low freq
    #BnH 63H 37H 62H 0AH 06H vv   medium high freq
    #BnH 63H 37H 62H 0BH 06H vv   high freq
    packet = [ 0xb0 | (channel & 0x0f), 0x63, 0x37, 0x62, 0x00, 0x06, (lowBand & 0x7f)];
    serialPort.write(bytearray(packet))
    packet[4] = 0x01;
    packet[6] = (medLowBand & 0x7f);
    serialPort.write(bytearray(packet))
    packet[4] = 0x02;
    packet[6] = (medHighBand & 0x7f);
    serialPort.write(bytearray(packet))
    packet[4] = 0x03;
    packet[6] = (highBand & 0x7f)
    serialPort.write(bytearray(packet))
    packet[4] = 0x08;
    packet[6] = (lowFreq & 0x7f)
    serialPort.write(bytearray(packet))
    packet[4] = 0x09;
    packet[6] = (medLowFreq & 0x7f)
    serialPort.write(bytearray(packet))
    packet[4] = 0x0A;
    serialPort.write(bytearray(packet))
    packet[4] = 0x0B;
    packet[6] = (highFreq & 0x7f)
    serialPort.write(bytearray(packet))

def setTuning(channel, coarse, fine): 
    # This will turn off any note playing on the channel
    #BnH 65H 00H 64H 01H 06H vv  Fine
    #BnH 65H 00H 64H 02H 06H vv  Coarse
    packet = [ 0xb0 | (channel & 0x0f), 0x65, 0x00, 0x64, 0x01, 0x06, (fine & 0x7f)];
    serialPort.write(bytearray(packet))
    packet[4] = 0x02
    packet[6] = (coarse & 0x7f)
    serialPort.write(bytearray(packet))

def setVibrate(channel, rate, depth, mod): 
    #BnH 63H 01H 62H 08H 06H vv  Rate
    #BnH 63H 01H 62H 09H 06H vv  Depth
    #BnH 63H 01H 62H 0AH 06H vv  Delay modify
    packet = [ 0xb0 | (channel & 0x0f), 0x63, 0x01, 0x62, 0x08, 0x06, (rate & 0x7f)];
    serialPort.write(bytearray(packet))
    packet[4] = 0x09
    packet[6] = (depth & 0x7f)
    serialPort.write(bytearray(packet))
    packet[4] = 0x0A
    packet[6] = (mod & 0x7f)
    serialPort.write(bytearray(packet))

def setTVF(channel, cutoff, resonance): 
    #BnH 63H 01H 62H 20H 06H vv  Cutoff
    #BnH 63H 01H 62H 21H 06H vv  Resonance
    packet = [ 0xb0 | (channel & 0x0f), 0x63, 0x01, 0x62, 0x20, 0x06, (cutoff & 0x7f)];
    serialPort.write(bytearray(packet))
    packet[4] = 0x21;
    packet[6] = (resonance & 0x7f)
    serialPort.write(bytearray(packet))

def setEnvelope(channel, attack, decay, release): 
    #BnH 63H 01H 62H 63H 06H vv
    #BnH 63H 01H 62H 64H 06H vv
    #BnH 63H 01H 62H 66H 06H vv
    packet = [ 0xb0 | (channel & 0x0f), 0x63, 0x01, 0x62, 0x63, 0x06, (attack & 0x7f)];
    serialPort.write(bytearray(packet))
    packet[4] = 0x64;
    packet[6] = (decay & 0x7f);
    serialPort.write(bytearray(packet))
    packet[4] = 0x66;
    packet[6] = (release & 0x7f);
    serialPort.write(bytearray(packet))

def setScaleTuning(channel, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12): 
    #F0h 41h 00h 42h 12h 40h 1nh 40h v1 v2 v3 ... v12 F7h
    # values are in range 00h = -64 cents to 7fh = +64 cents, center is 40h
    packet = [  0xf0, 0x41, 0x00, 0x42, 0x12, 0x40, 0x10 | (channel & 0x0f), 0x40,
        v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, 0xf7];
    serialPort.write(bytearray(packet))

def allDrums(): 
    #F0h 41h 00h 42h 12h 40h 1ph 15h vv xx F7h
    packet = [  0xf0, 0x41, 0x00, 0x42, 0x12, 0x40, 0x10, 0x15, 0x01, 0x00, 0xf7];
    serialPort.write(bytearray(packet))
    for i in range (1, 15): 
        packet[6] = i;
        serialPort.write(bytearray(packet))


