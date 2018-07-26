#!/usr/bin/python

import spidev

spi=spidev.SpiDev()
spi.open(0, 0)
spi2=spidev.SpiDev()
spi2.open(0, 1)

def read(channel):
    if channel >15 or channel<0:
        return -1
    if channel < 8:
        r=spi.xfer2([1, 8+channel<<4, 0])
    else:
        r=spi2.xfer2([1, 8+(channel-8)<<4, 0])
    v=((r[1]&3)<<8)+r[2]

    return v
