import argparse
import mbt
from mbt import __version__


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('micro-backup-tool')
    version = '%(prog)s ' + __version__
    parser.add_argument('--version', '-v', action='version', version=version)
    parser.add_argument('--dirs', '-d', action='dirs', version=version)
    return parser


def main(args=None):
    """
    Main entry point for your project.

    Args:
        args : list
            A of arguments as if they were input in the command line. Leave it
            None to use sys.argv.
    """

    parser = get_parser()
    args = parser.parse_args(args)

    print(args)

    # Put your main script logic here
    print('No action defined for mbt module!')


if __name__ == '__main__':
    main()
