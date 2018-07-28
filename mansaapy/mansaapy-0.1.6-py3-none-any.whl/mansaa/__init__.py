from bluepy import btle

class mansaa:
    def __init__(self, mac):
        self.address = mac
    
    def connect(self):
        try:
            self.device = btle.Peripheral(self.address)
            characteristics = self.device.getCharacteristics()
            for characteristic in characteristics:
                if characteristic.uuid == "0000ffb1-0000-1000-8000-00805f9b34fb":
                    self.ctrlChr = characteristic
                elif characteristic.uuid == "0000ffb2-0000-1000-8000-00805f9b34fb":
                    self.colorChr = characteristic

            # Set bulb to default mode
            # self.ctrlChr.write(bytearray([0x00, 0x00, 0x00, 0x1e]), withResponse=True)

            # Read current color values from the bulb
            colorBytes = self.colorChr.read()

        except Exception as e:
            print ("Error in connecting")
            print (e)
            # raise ValueError("Unable to connect")

    def setColor(self, color):
        try:
            self.colorChr.write(bytearray([0xd0, color[0], color[1], color[2]]), withResponse=True)
        except Exception as e:
            print('Error while writing to bulb')
            print(e)
            raise ValueError('Could not write value')

    def getState(self):
        colorBytes = None
        try:
            colorBytes = self.colorChr.read()
        except Exception as e:
            print ("Error while reading value")
            print (e)
        return colorBytes