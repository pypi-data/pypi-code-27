import logging
import serial

sho_logger = logging.getLogger("shongololo_log_file")


def open_imets(devices):
    """Tries to open as many imet device serial ports as there are
    :param devices: a list of socket paths
    :return: a list of socket handles
    """
    imet_sockets = []
    for d in devices:  # Create list of imet open ports
        try:
            ser = serial.Serial(d[0], baudrate=57600, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS,
                                stopbits=serial.STOPBITS_ONE, timeout=3.0, xonxoff=False)
            imet_sockets.append(ser)
            sho_logger.info("\n Successfully opened Imet device on port {}".format(d))

        except serial.SerialException as e:
            sho_logger.error(e)
            sho_logger.critical("\nFailed to open imet on port {}".format(d))

    return imet_sockets
