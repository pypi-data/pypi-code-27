# Command-line runner, installed using setup tools
# to provide globally available `pmail` command.
import sys
from pmail.run import run


# Script entry point
def main(arguments=None):
    try:
        run(arguments or sys.argv[1:])
    except KeyboardInterrupt:
        quit()


# Run if script executed directly, pass the received command-line arguments
if __name__ == '__main__':
    main(sys.argv[1:])
