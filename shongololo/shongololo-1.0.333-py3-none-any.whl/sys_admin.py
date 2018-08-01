# sys_admin.py
import os
import sys
import datetime
import logging
import subprocess
import time
import serial

import shongololo.K30_serial as KS

# import serial.tools.list_ports as port
"""File of system administrative functions and default config settings"""
sho_logger = logging.getLogger("shongololo_log_file")


def close_sensors(socks):
    """
    Closes sensor sockets"
    :type socks: serial.Serial
    """
    for s in socks:
        try:
            s.close()
        except serial.SerialException as e:
            sho_logger.error(e)
        sys.stdout.flush()
    sho_logger.info("Closed Sensors")

def shutdown_monitor():
    """Just logs a message that everything has been shutdown"""
    sho_logger.info("Shutting down Logger")
    handlers = sho_logger.handlers[:]
    for handler in handlers:
            handler.close()
            sho_logger.removeHandler(handler)

# Functions for stand alone instance
def stop_file(a_file, msg):
    a_file.write(msg)
    a_file.close()


def shutdown(imets, k30s):
    for i in imets:
        i.close()
    for k in k30s:
        k.close()


def if_mk_dir(directory):
    """Check if a given directory is present and if not create it.
    :type directory: str
    :param directory: Full path to directory being queried
    """
    try:
        os.listdir(directory)
    except NotImplementedError or PermissionError as e:
        # sho_logger.error(e)
        # sho_logger.info("Due to above error exiting, try correcting the issue and restarting the application.")
        sys.exit()
    except FileNotFoundError:
        # sho_logger.info("{} directory not present creating it".format(directory))

        try:
            os.mkdir(directory)
        except PermissionError or FileExistsError as e:
            # sho_logger.error('Error creating directory {0}.  {1}'.format(directory, e))
            # sho_logger.info("Due to above error exiting, try correcting the issue and restarting the application.")
            sys.exit()

        # sho_logger.info("Successfully created {} directory".format(directory))
        return

    # sho_logger.info("Data directory is already present at {}".format(directory))
    return


def mk_numbered_nd(new_dir):
    """
    Make a new directory with a name corresponding to the current system date and sample session number
    :param new_dir: Full path to destination folder ending in '/'
    :return: A tuple of (Status int, new_numbered_directory str).  Non-zero status indicates an error
    """
    dt = str(datetime.datetime.today())[0:10]
    try:
        folders = os.listdir(new_dir)
    except PermissionError or FileNotFoundError as e:
        sho_logger.error("{}\n Unable to access given directory due to above.  Data will not be recorded.  Recommend "
                         "addressing the error and restarting the application".format(e))
        return -1

    num = len(folders)
    numbered_new_dir = new_dir + dt + "CAPTURE_" + str(num).zfill(3)

    try:
        os.mkdir(numbered_new_dir)

    except PermissionError as e:
        sho_logger.error("Failed to create new directory {0}\n Error:{1}".format(numbered_new_dir, e))
        return -1, ""

    # sho_logger.info("Successfully created {}".format(numbered_new_dir))
    return 0, numbered_new_dir + "/"


def set_system_time(imet_device):
    """
    Captures a date and time and sets the inputs as the system date and time.
    """
    try:
        # For some reason 1st read often fails without even throwing exception so try twice just to be safe
        imet_device.readline()
        time.sleep(0.5)
        data_line = imet_device.readline()

    except IOError as e:
        sho_logger.error("Unable read time from Imet device: %s.  Error: %s", imet_device, e)
        return -1

    i_time = str(data_line).split(',')[5:7]
    i_date = i_time[0].replace('/', '')
    i_hour = i_time[1]
    po = subprocess.Popen("sudo date +%Y%m%d -s {}".format(i_date), stdout=subprocess.PIPE, shell=True)
    (output, err) = po.communicate()
    p_status1 = po.wait()
    po = subprocess.Popen("sudo date +%T -s {}".format(i_hour), stdout=subprocess.PIPE, shell=True)
    (output, err) = po.communicate()
    p_status2 = po.wait()

    if (p_status1+p_status2) != 0:
        sho_logger.error("Failed to set system time: " + output.decode("utf-8"))
        sho_logger.info("System time is: {}".format(datetime.datetime.now()))
        return -1
    else:
        sho_logger.info("Attempt to set date to: {0} {1}".format(i_time[0],i_hour))
        sho_logger.info("System time is: {}".format(datetime.datetime.now()))
        return 0


def ini_datafile(filename, header):
    """
    Make this session's data directory, open it's data file, and write a header
    :param filename: The full path string you want the file to be called and located at
    :param header: String defining the first line of the file: expected to be comma separated variable names
    :return: the file handler
    """
    fd = None
    try:
        fd = open(filename, 'w+')
        fd.write(header)
        sho_logger.info("Started data log file")
        sys.stdout.flush()
    except IOError:
        sho_logger.error("Failed to open data logging file")

    return fd


def read_data(i_socks, k_socks):
    """
    Do the actual work of reading for all sensors
    :param i_socks: list of imet_open sockets
    :param k_socks: list of k30 open sockets
    :return: a single list of outputs from all sensors read
    """
    # TODO convert this to a threaded approach of parallel sensor reading
    latest_k_data = []
    latest_i_data = []
    for k in k_socks:
        reading = KS.read_ppm(k)
        latest_k_data.append(reading)
    for i in i_socks:
        im_values = i.readline()
        latest_i_data.append(str(im_values)[5:-5])
    return latest_i_data, latest_k_data


def find_devices():
    """
    Find available serial device sensors
    :return:Dictionary of devices in type lists of tuples (<path>,<id>)
    devices = {'k30s': [('/dev/ttyUSB1', 'A')], 'imets': [], 'pixhawks': []}
    """
    # Ids of USB ports found on a Pi3B+  possible differs on other devices
    ids = {"2": "A", "4": "B", "3": "C", "5": "D"}
    k30_product_id = "ea60"
    imet_product_id = "6015"
    # TODO get actual Pixhawk product ID and add to search
    pixhawk_product_id = "BEEF"
    devices = {"k30s": [], "imets": [], "pixhawks": []}
    ports = []

    # Find all serial usb devices
    devs = os.listdir("/dev/")
    for d in devs:
        if "ttyUSB" in d:
            ports.append("/dev/" + d)

    # Search for each product id
    for p in ports:
        po = subprocess.Popen('/sbin/udevadm info -a  --name={}'.format(p), stdout=subprocess.PIPE, shell=True)
        (output, err) = po.communicate()
        po_status = po.wait()
        output = str(output)

        if po_status == 0:
            if 'ATTRS{{idProduct}}=="{}"'.format(k30_product_id) in output:
                po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="1.\''.format(p),
                                      stdout=subprocess.PIPE, shell=True)
                (output, err) = po.communicate()
                po.wait()

                # Pulls kernel identification of usb port from response
                try:
                    port_id = ids[str(output).split("\\n")[1][-2:-1]]
                except KeyError as e:
                    sho_logger.error("KeyError raised: {}".format(str(e)))
                    port_id = "X"
                except IndexError as e:
                    sho_logger.error("IndexError raised: {}".format(str(e)))
                    port_id = "X"
                devices["k30s"].append((p, port_id))

            elif 'ATTRS{{idProduct}}=="{}"'.format(imet_product_id) in output:
                po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="1.\''.format(p),
                                      stdout=subprocess.PIPE, shell=True)
                (output, err) = po.communicate()
                po.wait()

                # Pulls kernel identification of usb port from response
                try:
                    port_id = ids[str(output).split("\\n")[1][-2:-1]]
                except KeyError as e:
                    sho_logger.error("KeyError raised: {}".format(str(e)))
                    port_id = "X"
                except IndexError as e:
                    sho_logger.error("IndexError raised: {}".format(str(e)))
                    port_id = "X"
                devices["imets"].append((p, port_id))

            elif 'ATTRS{{idProduct}}=="{}"'.format(pixhawk_product_id) in output:
                po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="1.\''.format(p),
                                      stdout=subprocess.PIPE, shell=True)
                (output, err) = po.communicate()
                po.wait()

                # Pulls kernel identification of usb port from response
                try:
                    port_id = ids[str(output).split("\\n")[1][-2:-1]]
                except KeyError as e:
                    sho_logger.error("KeyError raised: {}".format(str(e)))
                    port_id = "X"
                except IndexError as e:
                    sho_logger.error("IndexError raised: {}".format(str(e)))
                    port_id = "X"
                devices["pixhawks"].append((p, port_id))

        else:
            sho_logger.error("Error, couldn't get udev information about ports")
            sho_logger.info("{}".format(output.decode("utf-8")))
            sho_logger.error(str(err))
            return -1
    sho_logger.info("Devices found: {}".format(devices))
    return 0, devices

def shutdown_computer():
    """Gracefully shutdown computer from flask front end"""
    sho_logger.info("Shutting Down Computer")
    os.system('/usr/bin/sudo systemctl poweroff')
