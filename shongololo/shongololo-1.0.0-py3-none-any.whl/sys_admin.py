# sys_admin.py
import os
import sys
import datetime
import logging
import subprocess
import time
import configparser
config = configparser.ConfigParser()
config.read("config.ini")

import shongololo.K30_serial as KS

#import serial.tools.list_ports as port
"""File of system administrative funtions and default config settings"""
sho_logger = logging.getLogger("shongololo_logger")

#TODO move these hard coded settings into a config file

def close_sensors(socks):
    """CLoses sensor sockets"""
    for s in socks:
        try:
            s.close()
        except:
            pass

def shutdown_monitor():
    """Just logs a message that everything has been shutdown"""
    sho_logger.info("Shutting down App")

# Functions for stand alone instance
def stop_file(afile,msg):
    afile.write(msg)
    sys.stdout.flush()
    afile.close()

def shutdown(imets,k30s):
    for i in imets:
        i.close()
    for k in k30s:
        k.close()

def clear_log(log):
    """Remove old logfile"""
    p = subprocess.Popen("> {}".format(log), stdout=subprocess.PIPE, shell=True)

def if_mk_DIR(dir):
    """Check if a given directory is present and if not create it.  No logging done as logger may not yet exist"""

    p = subprocess.Popen("ls {}".format(dir), stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    if p_status !=0:
        sho_logger.info("{} directory not present creating it".format(dir))
        p = subprocess.Popen("mkdir {}".format(dir), stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if p_status == 0:
            sho_logger.info("Created {} directory".format(dir))
            return 0
        else:
            sho_logger.error('Error creating directory {0}.  {1}'.format(dir, output))
            return -1
    else:
        sho_logger.info("Data directory present at {}".format(dir))
        return 0

def mk_ND(new_dir):
    """
    Make a new directory with name corresponding to session number
    """
    dt = str(datetime.datetime.today())[0:10]
    p = subprocess.Popen("ls {}".format(new_dir), stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    print(str(output))
    print(str(output).split("\n"))
    num=len(str(output).split("\\n"))
    print(str(num))
    print(str(num).zfill(3))
    ND=new_dir+dt+"CAPTURE_"+str(num).zfill(3)

    p = subprocess.Popen("mkdir -p {}".format(ND), stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()
    if p_status == 0:
        sho_logger.info("Successfully created new %s", ND)
        return 0, ND+"/"
    else:
        sho_logger.error("Failed to create new directory {}".format(ND))
        return -1, ""


def set_system_time(imet_device):
    """
    Captures a date and time and sets the inputs as the system date and time.
    Minimal date entry santitisation performed
    """
    try:
        #For some reason 1st reason often fails without even throwing exception so try twice just to be safe
        l = imet_device.readline()
        time.sleep(0.5)
        l = imet_device.readline()

    except IOError as e:
        sho_logger.error("Unable read time from Imet device: %s.  Error: %s", imet_device, e)
        return -1

    i_time= str(l).split(',')[5:7]
    idate=i_time[0].replace('/','')
    ihour=i_time[1]
    p = subprocess.Popen("sudo date +%Y%m%d -s {}".format(idate), stdout=subprocess.PIPE, shell=True)
    sho_logger.info("Attempt to set date to: {}".format(idate))
    (output, err) = p.communicate()
    p_status = p.wait()

    if p_status !=0:
        sho_logger.error("Failed to set system time: "+output+" "+err+" "+p_status)
        return -1
    else:
        sho_logger.info("Set system time: {}".format(output))
        return 0

def ini_datafile(filename, header):
    """
    Make this session's data directory, open it's data file, and write a header
    :param filename: The full path string you want the file to be called and located at
    :return: the file handler
    """
    try:
        fd = open(filename,'w+') 
        fd.write(header)
        sho_logger.info("Started data log file")
        sys.stdout.flush()
    except IOError:
        sho_logger.error("Failed to open data logging file" )

    return  fd

def read_data(isocks, ksocks):
    """
    Do the actual work of reading for all sensors
    :param isocks: list of imet_open sockets
    :param ksocks: list of k30 open sockets
    :return: a single list of outputs from all sensors read
    """
    #TODO convert this to a threaded approach of parallel sensor reading
    latestkdata = []
    latestidata = []
    for k in ksocks:
        reading = KS.read_ppm(k)
        latestkdata.append(reading)
    for i in isocks:
        im_values = i.readline()
        latestidata.append(str(im_values)[5:-5])
    return latestidata, latestkdata

def find_devices():
    """
    Find available serial device sensors
    :return:Dictionary of devices in type lists of tuples (<path>,<id>)
    devices = {'k30s': [('/dev/ttyUSB1', 'A')], 'imets': [], 'pixhawks': []}
    """
    # Ids of USB ports found on a Pi3B+  possible differes on other devices
    ids = {"2": "A", "4": "B", "3": "C", "5": "D"}
    portID = "X"
    K30_productID = "ea60"
    Imet_productID = "6015"
    # TODO get actual Pixhawk product ID and add to search
    Pixhawk_productID = "BEEF"
    devices = {"k30s": [], "imets": [], "pixhawks": []}

    # Find all serial usb devices
    p = subprocess.Popen("ls /dev/ttyUSB*", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    ports = str(output).split("\\n")[:-1]
    ports[0] = ports[0][2:]

    if p_status == 0:
        # Search for each product id
        for d in ports:
            p = subprocess.Popen('udevadm info -a  --name={}'.format(d), stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            output=str(output)

            if p_status == 0:
                if 'ATTRS{{idProduct}}=="{}"'.format(K30_productID) in output:
                    p = subprocess.Popen('udevadm info -a  --name={} | grep \'KERNELS=="1.\''.format(d),
                                         stdout=subprocess.PIPE, shell=True)
                    (output, err) = p.communicate()
                    p.wait()

                    # Pulls kernel identification of usb port from response
                    try:
                        portID = ids[str(output).split("\\n")[1][-2:-1]]
                        devices["k30s"].append((d, portID))
                    except KeyError as e:
                        sho_logger.error("KeyError raised: {}".format(str(e)))
                    except IndexError as e:
                        sho_logger.error("IndexError raised: {}".format(str(e)))


                elif 'ATTRS{{idProduct}}=="{}"'.format(Imet_productID) in output:
                    p = subprocess.Popen('udevadm info -a  --name={} | grep \'KERNELS=="1.\''.format(d),
                                         stdout=subprocess.PIPE, shell=True)
                    (output, err) = p.communicate()
                    p.wait()

                    # Pulls kernel identification of usb port from response
                    try:
                        portID = ids[str(output).split("\\n")[1][-2:-1]]
                        devices["imets"].append((d, portID))
                    except KeyError as e:
                        sho_logger.error ("KeyError raised: {}".format(str(e)))
                    except IndexError as e:
                        sho_logger.error ("IndexError raised: {}".format(str(e)))

                elif 'ATTRS{{idProduct}}=="{}"'.format(Pixhawk_productID) in output:
                    p = subprocess.Popen('udevadm info -a  --name={} | grep \'KERNELS=="1.\''.format(d),
                                         stdout=subprocess.PIPE, shell=True)
                    (output, err) = p.communicate()
                    p.wait()

                    # Pulls kernel identification of usb port from response
                    try:
                        portID = ids[str(output).split("\\n")[1][-2:-1]]
                        devices["pixhawks"].append((d, portID))
                    except KeyError as e:
                        sho_logger.error ("KeyError raised: {}".format(str(e)))
                    except IndexError as e:
                        sho_logger.error ("IndexError raised: {}".format(str(e)))

            else:
                sho_logger.error("Error, couldn't get udev information about ports")
                return -1
        return 0, devices
    else:
        sho_logger.error("Error: couldn't access prots, most likely this is a permissions issue or no sensors are plugged in")
        return -1
