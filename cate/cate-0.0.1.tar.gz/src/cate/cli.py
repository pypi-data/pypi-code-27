# -*- coding: utf-8 -*-

"""
Logic to handle the Command Line Interface (CLI).
"""

import argparse
import json
import logging
import logging.config
import os
import os.path
import textwrap

from . import main
from . import __name__ as pkgname  # name of the main package (i.e., the app)
from . import __version__


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


# XXX: SCALE_BOUNDS constant tuple introduces a strong coupling between this
# module and the drawing module: consider defining the constant tuple in the
# drawing module and importing it.
SCALE_BOUNDS = (0.5, 3.0)


def _bounded_float(inf, sup):
    """
    Create a suitable callable for `argparse.add_argument` `type=` argument.

    The returned callable converts the string into a float, and checks the
    converted value falls within [inf, sup] (inclusive set).
    """
    def _type(string):
        value = float(string)
        if value < inf or value > sup:
            msg = '{} does not fall within [{}, {}].'.format(value, inf, sup)
            raise argparse.ArgumentTypeError(msg)
        return value
    return _type


def _parse_args(args=None):
    """
    Parse the arguments of the command line.

    This is a wrapper around `argparse.ArgumentParser` that creates a suitable
    parser for our usage.  As for `argparse.ArgumentParser.parse_args`, `args`
    defaults to `sys.argv`.
    """
    parser = argparse.ArgumentParser(
        prog=pkgname,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Draw the templates of chaotic attractors.',
        epilog=textwrap.dedent(
            f'''
            To read a matrix from a file whose name starts with a '-' for example
            '-foo.json', use one of these commands:
              {pkgname} -- -foo.json

              {pkgname} ./-foo.json
            '''
        ),
    )
    parser.add_argument(
        '--version',
        action='version',
        version='{} {}'.format(pkgname, __version__),
    )
    parser.add_argument(
        '-s', '--scale',
        default=1.0,
        type=_bounded_float(*SCALE_BOUNDS),
        help='Alter scale of the template.' \
            ' The scale value must reside between {} and {}.'.format(*SCALE_BOUNDS),
    )
    parser.add_argument(
        '-t', '--complete-flow',
        action='store_true',
        help='Add semicircles depicting the complete flow of the attractor.',
    )
    parser.add_argument(
        '-c', '--no-color',
        action='store_false',
        help='Do not color the template.',
        dest='color',
    )
    parser.add_argument(
        '-o', '--output',
        default='template.svg',
        help='Set the output filename to OUTPUT.' \
            ' Default output filename is \'template.svg\'.' \
            ' Use \'-\' to output the matrix to stdout.',
    )
    parser.add_argument(
        'matrix',
        help='Filename to read the matrix from.' \
            ' The matrix must be encoded as a JSON array of arrays.' \
            ' Use \'-\' to read the matrix from stdin.',
    )
    return parser.parse_args(args)


def _setup_logging():
    """
    Configure the logging.

    The default logging behavior can be tweaked through the environment
    variable `CATE_LOG_CFG`.
    To modify the configuration of the logging, the environment variable
    `CATE_LOG_CFG` has to point to a JSON file that is a valid configuration
    dictionary.  Do not modify the logging configuration unless you know what
    you are doing!

    See https://docs.python.org/3/library/logging.config.html for more details
    on the configuration of the logging module.
    """
    log_cfg_filename = os.getenv('CATE_LOG_CFG')
    if log_cfg_filename is not None and os.path.isfile(log_cfg_filename):
        with open(log_cfg_filename, mode='rt') as log_cfg_fd:
            log_cfg = json.load(log_cfg_fd)
        logging.config.dictConfig(log_cfg)
    else:
        logging.basicConfig(
            # levelname is padded with spaces to the length of the longest levelname
            format='[{levelname:^8}] {message}',
            style='{',
            level=logging.INFO,
        )


def cli():
    """Entry point for the Command Line Interface (CLI)."""
    _setup_logging()
    options = vars(_parse_args())  # read argparse.Namespace as a dict
    logger.debug(f'parsed arguments: {options}')
    infile = options.pop('matrix')  # extract positional argument from options
    main.run(infile, **options)
