import sys
import time
from global_vars import imu
from commands import OpenIMU_CLI

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    print("This is openimu main routine.")
    imu.find_device()
    cli = OpenIMU_CLI() 
    cli.command_handler()

if __name__ == "__main__":
    main()
