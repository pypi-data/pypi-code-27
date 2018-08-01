# start_up.py
import logging
import time
import sys

import shongololo.K30_serial as KS
import shongololo.sys_admin as SA
import shongololo.Imet_serial as IS


def start_logging(log_name="shongololo.log", flask_handler=None, stdout=1):
    """Setup logging according to use case
    :type log_name: str
    :param log_name: file name for logfile
    :param flask_handler:
    :param stdout: 1: don't output to stdout but any other number do
    """
    # Setup Application Logging
    sho_logger = logging.getLogger("shongololo_log_file")
    sho_logger.setLevel(logging.DEBUG)

    sho_file_handler = logging.FileHandler(log_name, mode="w")
    sho_file_handler.setLevel(logging.DEBUG)
    sho_file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d"))
    sho_logger.addHandler(sho_file_handler)

    if stdout != 1:
        sho_stream_handler = logging.StreamHandler(sys.stdout)
        sho_stream_handler.setLevel(logging.DEBUG)
        sho_stream_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d"))
        sho_logger.addHandler(sho_stream_handler)

    if flask_handler is not None:
        sho_logger.addHandler(flask_handler)
        sho_logger.info("Started logging with flask handler")
    else:
        sho_logger.info("Started logging without flask handler")


def start_up():
    # TODO capture_duration of run =
    """ Perform startup functions
    Optionally accepts a flask socket handler for when being used by a flask web interface
    :returns
    2 lists of open serial sockets to first imet and then k30 sensors
"""
    sho_logger = logging.getLogger("shongololo_log_file")
    # Access devices
    status, device_dict = SA.find_devices()

    if status != 0:
        sho_logger.error("Problem accessing devices, exiting")
        sys.exit()

    else:
        # Connect to imets 1st so can set system time and create data directory
        imet_sockets = IS.open_imets(device_dict["imets"])

        # If imets present try setting system time to UTC
        if len(imet_sockets) != 0:
            SA.set_system_time(imet_sockets[0])
        else:  # Don't bother trying to get and set time from Imet
            sho_logger.error(
                "Due to no Imet devices present system time and consequently data time stamps will be based current "
                "system time: {0}".format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        # Connect to CO2 meters
        k30_sockets = KS.open_k30s(device_dict["k30s"])

        return imet_sockets, k30_sockets, device_dict


def test_sensors(i_sockets, k_sockets):
    """Trying reading data from sensors"""
    sho_logger = logging.getLogger("shongololo_log_file")
    sho_logger.info("Attempting to read from all sensors.")
    if len(k_sockets) == 0 and len(i_sockets) == 0:
        sho_logger.info("No sensors found please attach sensors and start again.")
        SA.close_sensors(i_sockets+k_sockets)
        return 1

    for k, sensor_id in zip(k_sockets, range(len(k_sockets))):
        try:
            ppm = KS.read_ppm(k)
            sho_logger.info("K30_sensor_{0}: CO2: {1}ppm".format(sensor_id, ppm))
        except IOError as e:
            sho_logger.error("Unable read K30 sensor: {0}.  Error: {1}".format(k, e))

    for i, sensor_id in zip(i_sockets, range(len(i_sockets))):
        try:
            im_values = i.readline()
            sho_logger.info("Imet_sensor_{0}: Values: {1}".format(sensor_id, im_values))
        except IOError as e:
            sho_logger.error("Unable read time from Imet device: {0}.  Error: {1}".format(i, e))

    sho_logger.info("Finished sensor test sequence.")
    return 0
