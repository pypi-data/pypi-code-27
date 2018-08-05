import argparse
import sys
from .core import get_renderer,enact_expressions

def main():
    parser = argparse.ArgumentParser(description='A command line utility to'
            ' interpret dice roll expressions')

    parser.add_argument('expressions', nargs='+',
            help='any expressions to parse and run')
    parser.add_argument('--renderer', dest='renderer', default='pretty',
            nargs='?',
            help='which renderer to use (default: pretty)')
    parser.add_argument('--pretty_json', dest='pretty_json',
            action='store_true',
            help='whether json should be human readable')

    args = parser.parse_args()

    try:
        renderer = get_renderer(args.renderer)
    except ImportError:
        print('no such renderer:', args.renderer)
        sys.exit(1)
    else:
        enact_expressions(args.expressions, renderer, args)
