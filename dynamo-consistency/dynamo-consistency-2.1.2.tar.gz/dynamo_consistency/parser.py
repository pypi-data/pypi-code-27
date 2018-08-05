"""
Module that parses the command line for dynamo-consistency
"""

import os
import sys

import optparse

from ._version import __version__

# My executables
EXES = ['dynamo-consistency', 'set-status', 'consistency-web-install']

def get_parser(modname='__main__',
               prog=os.path.basename(sys.argv[0])):
    """
    :param str modname: The module to fetch the ``__doc__`` optionally ``__usage__`` from.
                        If you want the parser for a particular file,
                        this would usually be ``__name__``
    :param str prog: The name for the program that we want the parser for

    :returns: A parser based on the program name and the arguments to pass it
    :rtype: optparse.OptionParser, list
    """

    mod = sys.modules[modname]
    usage = '%s\n%s' % (mod.__usage__, mod.__doc__) if '__usage__' in dir(mod) else None

    parser = optparse.OptionParser(usage=usage, version='dynamo-consistency %s' % __version__)

    # Don't add all the options to help output for irrelevant scripts
    add_all = prog == 'dynamo-consistency' or (
        '-h' not in sys.argv and '--help' not in sys.argv and (
            prog == 'sphinx-build' or 'sphinx' not in sys.modules
            )
        )

    parser.add_option('--config', metavar='FILE', dest='CONFIG',
                      help='Sets the location of the configuration file to read.')
    if add_all:
        parser.add_option('--site', metavar='PATTERN', dest='SITE_PATTERN',
                          help='Sets the pattern used to select a site to run on next.')


    log_group = optparse.OptionGroup(parser, 'Logging Options')

    if add_all:
        log_group.add_option('--email', action='store_true', dest='EMAIL',
                             help='Send an email on uncaught exception.')

    log_group.add_option('--info', action='store_true', dest='INFO',
                         help='Displays logs down to info level.')

    log_group.add_option('--debug', action='store_true', dest='DEBUG',
                         help='Displays logs down to debug level.')

    parser.add_option_group(log_group)


    backend_group = optparse.OptionGroup(
        parser, 'Behavior Options',
        'These options will change the backend loaded and actions taken')

    if add_all:
        backend_group.add_option('--cms', action='store_true', dest='CMS',
                                 help='Run actions specific to CMS collaboration data.')
        backend_group.add_option('--unmerged', action='store_true', dest='UNMERGED',
                                 help='Run actions on "/store/unmerged".')

    backend_group.add_option('--v1', action='store_true', dest='V1',
                             help='Connect to Dynamo from outside with old Dynamo libraries')
    backend_group.add_option('--test', action='store_true', dest='TEST',
                             help='Run with a test instance of backend module.')

    parser.add_option_group(backend_group)


    argv = sys.argv if prog in EXES else [arg for arg in sys.argv if arg in ['--debug', '--info']]
    if prog.startswith('test_'):
        argv.append('--test')

    return parser, argv


PARSER, ARGV = get_parser()

OPTS, ARGS = PARSER.parse_args(ARGV)

if not os.path.basename(sys.argv[0]) == 'sphinx-build':
    def pretty_exe(_):
        """A dummy since we don't care about the docs here"""
        pass

else:
    import inspect
    # We only get here while running Sphinx.
    # In that case, you should also install what's in docs/requirements.txt
    from customdocs import pretty_exe_doc  #pylint: disable=import-error

    def pretty_exe(name):
        """
        Modifies the calling module's doc string
        :param str name: The desired heading for the new docstring
        """

        mod = inspect.getmodule(inspect.stack()[1][0])
        pretty_exe_doc(name, lambda: get_parser(mod.__name__, name)[0], 2)
