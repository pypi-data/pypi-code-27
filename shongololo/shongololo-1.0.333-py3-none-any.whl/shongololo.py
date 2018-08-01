# shongololo.py
""" Collect data from CO2 meters on Pi3 USB ports via serial to FTDI cables """
import time
import sys
import logging
import getpass

import shongololo.sys_admin as SA
import shongololo.start_up as SU

# TODO enable following with pkg_resources module later
user = getpass.getuser()
data_dir = '/home/' + user + '/DATA/'
logfile = data_dir+'Shongololo_log.log'
datafile = 'data.csv'
period = 0.5
i_head = ",IMET_ID,  Latitude, Longitude, Altitude, Air Speed (m/s), Mode, Fixed Satellites, Available Satellites," \
        "voltage,current,level,id "
k_head = ",K30_ID, CO2 ppm"

if __name__ == "__main__":

    # Start up services
    SA.if_mk_dir(data_dir)
    SU.start_logging(logfile, None, 0)
    sho_logger = logging.getLogger("shongololo_log_file")
    i_socks, k_socks, device_dict = SU.start_up()
    if SU.test_sensors(i_socks, k_socks) == 1:
        sho_logger.info("No sensors present, quitting")
        SA.close_sensors(i_socks + k_socks)
        sys.exit()

    # Start data file
    status, new_data_dir = SA.mk_numbered_nd(data_dir)
    if status != 0:
        sho_logger.error("Failed to create directory for data logging, data will not be saved to file, try restarting "
                         "the application")
        sys.exit()

    else:
        header = ""
        for c in range(len(device_dict["k30s"])):
            header = header + str(k_head)
        for i in range(len(device_dict["imets"])):
            header = header + str(i_head)
        fd = SA.ini_datafile(str(new_data_dir) + datafile, header)

        # PRIMARY LOOP
        while 1:
            pack = []
            data_line = ""
            try:
                latest_imet_data, latest_k30_data = SA.read_data(i_socks, k_socks)

                # Pack data
                for count, k in zip(range(len(device_dict["k30s"])), device_dict["k30s"]):
                    pack.append(k[1] + "," + latest_k30_data[count])

                for count, i in zip(range(len(device_dict["imets"])), device_dict["imets"]):
                    pack.append(i[1] + "," + latest_imet_data[count])

                for x in pack:
                    data_line = data_line + "," + x

                fd.write("\n" + data_line)
                sho_logger.info(data_line)

                time.sleep(period)

            except KeyboardInterrupt as e:
                SA.close_sensors(i_socks + k_socks)
                SA.stop_file(fd, "\nKeyboard Interrupt: System stopped, closing down and saving data")
                sys.exit()
