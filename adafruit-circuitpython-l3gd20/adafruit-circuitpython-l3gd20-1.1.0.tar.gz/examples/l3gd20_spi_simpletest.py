import time
from board import SCK, MISO, MOSI, D5
import busio
import digitalio
import adafruit_l3gd20

# define the spi conneciton
CS = digitalio.DigitalInOut(D5)  # select pin is 5
SPIB = busio.SPI(SCK, MOSI, MISO)
# now initialize the device
SENSOR = adafruit_l3gd20.L3GD20_SPI(SPIB, CS)

while True:

    print('Acceleration (m/s^2): {}'.format(SENSOR.acceleration))

    print()

    #sleep for 1 second
    time.sleep(1)
