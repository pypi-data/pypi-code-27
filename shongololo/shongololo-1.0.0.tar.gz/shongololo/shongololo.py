# shongololo.py
""" Collect data from CO2 meters on Pi3 USB ports via serial to FTDI cables """
import time
import sys
import logging
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
datafile = config['DEFAULTS']['DATAFILE']
datadir = config['DEFAULTS']['DATADIR']
period = float(config['DEFAULTS']['PERIOD'])
ihead=config['DEFAULTS']['IMET_HEADER']
khead=config['DEFAULTS']['K30_HEADER']

import shongololo.sys_admin as SA
import shongololo.start_up as SU

#def main ():
#    print("I ran main")

if __name__ == "__main__":

    #Start up services
    isocks, ksocks, device_dict = SU.start_up(None)
    # Start data file
    status, ND = SA.mk_ND(datadir)
    sho_logger = logging.getLogger("shongololo_logger")
    if status !=0:
        sho_logger.error("Failed to create directory for data logging, data will not be saved to file, try restarting the application")
        sys.exit()

    else:
        print("HHHHHHHHHHHHH")
        print(ND) 
        print(str(ND)+datafile)
        header=""
        for c in range(len(device_dict["k30s"])):
            header=header+str(khead)
        for i in range(len(device_dict["imets"])):
            header=header+str(ihead)
        fd = SA.ini_datafile(str(ND)+datafile,header)
        
       # PRIMARY LOOP
        while 1:
            pack=[]
            dataline=""
            try:
                latest_idata, latest_kdata = SA.read_data(isocks, ksocks)
                
                #packdata
                for count, k in zip(range(len(device_dict["k30s"])),device_dict["k30s"]):
                    pack.append(k[1]+","+latest_kdata[count])

                for count, i in zip(range(len(device_dict["imets"])),device_dict["imets"]):
                    pack.append(i[1]+","+latest_idata[count])

                for x in pack:
                    dataline=dataline+","+x

                fd.write("\n"+dataline)
                print("\n"+dataline)

                time.sleep(period)

            except KeyboardInterrupt as e:
                SA.close_sensors(isocks+ksocks)
                SA.stop_file(fd, "\nKeyboard Interrupt: System stopped, closing down and saving data")
                sys.exit()

