import sys
from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '-l',
    '--log-file',
    metavar='FILE',
    default=sys.stdout,
    type=FileType('w'),
    help='Log file'
)
parser.add_argument(
    '-L',
    '--log-level',
    metavar='LEVEL',
    default='INFO',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help='Logging level'
)
parser.add_argument(
    '-F',
    '--log-format',
    metavar='FORMAT',
    default='[%(asctime)s] %(name)s.%(levelname)s: %(message)s',
    help='The logging format'
)
