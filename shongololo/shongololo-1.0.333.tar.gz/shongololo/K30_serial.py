import time
import logging
import serial
import sys

sho_logger = logging.getLogger("shongololo_log_file")


def read_ppm(socket):
    """
    Read data from a CO2 meter and return both the scaled result in ppm and a time stamp from when the reading was
    :param socket: open socket to K30 device
    :return: returns tuple of strings: time stamp, CO2 ppm value
    """
    # Python2
    # socket.write("\xFE\x44\x00\x08\x02\x9F\x25")
    # Python3
    socket.write(b'\xFE\x44\x00\x08\x02\x9F\x25')
    time.sleep(.1)
    resp = socket.read(7)
    try:
        # Python2
        # high = ord(resp[3])
        # low = ord(resp[4])
        # co2 = (high * 256) + low
        # Python3
        co2 = (resp[3] * 256) + resp[4]

    except IndexError:
        e = sys.exc_info()
        sho_logger.error("Unexpected errors reading from socket{0} \n Error: {1}".format(socket, e))
        return
    return str(co2)


def open_k30s(devices):
    """
    Tries to open as many K30 device serial ports as there are
    :param devices: list of device paths
    :return: a list of socket handles
    """

    k30_sockets = []
    for d in devices:
        try:
            ser = serial.Serial(d[0], baudrate=9600, timeout=.5)
            k30_sockets.append(ser)
            sho_logger.info("Successfully opened K30 on port {}".format(d))
        except serial.SerialException as e:
            sho_logger.error(e)
            sho_logger.error("Failed to open k30 on port {}".format(d))
    return k30_sockets
