"""
Module that parses the command line for dynamo-consistency
"""

import sys

from optparse import OptionParser


_PARSER = OptionParser("""%prog [options]

This program runs the Site Consistency Check for
Dyanmo Dynamic Data Management System.
See https://ddm-dynamo.readthedocs.io
for information about Dynamo and
http://dynamo-consistency.readthedocs.io
for information about this tool.""")


_PARSER.add_option('--config', metavar='FILE', dest='CONFIG',
                   help='Sets the location of the configuration file to read.')

_PARSER.add_option('--site', metavar='PATTERN', dest='SITE_PATTERN',
                   help='Sets the pattern used to select a site to run on next.')

_PARSER.add_option('--test', action='store_true', dest='TEST',
                   help='Run with a test instance of backend module.')

_PARSER.add_option('--cms', action='store_true', dest='CMS',
                   help='Run actions specific to CMS collaboration data.')

_PARSER.add_option('--unmerged', action='store_true', dest='UNMERGED',
                   help='Run actions on "/store/unmerged".')

_PARSER.add_option('--debug', action='store_true', dest='DEBUG',
                   help='Displays logs down to debug level.')

_PARSER.add_option('--info', action='store_true', dest='INFO',
                   help='Displays logs down to info level.')

_PARSER.add_option('--email', action='store_true', dest='EMAIL',
                   help='Send an email on uncaught exception.')


def _filter_args():
    """
    Filters out arguments so that only ones valid for this module's parser are passed.
    This is useful when running things like external tests or Sphinx
    :returns: Valid arguments from `sys.argv`
    :rtype: list
    """

    output = []
    last_action = ''

    for arg in sys.argv:

        if last_action == 'store':
            last_action = ''
            output.append(arg)

        for opt in _PARSER.option_list:
            if arg == opt.get_opt_string():
                last_action = opt.action
                output.append(arg)

    return output


# Filter out erroneous arguments only if something else is running this
(_OPTS, _) = _PARSER.parse_args(
    sys.argv if _PARSER.get_prog_name() == 'dynamo-consistency' else _filter_args())

_THIS = sys.modules[__name__]

# Put all destination arguments into module scope

for var in dir(_OPTS):
    if var.isupper():
        setattr(_THIS, var, getattr(_OPTS, var))
