# encoding: utf-8

"""
apimeter.compat
~~~~~~~~~~~~~~~~~

This module handles import compatibility issues between Python 2 and
Python 3.
"""

import sys
# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

try:
    import simplejson as json
except ImportError:
    import json  # noqa

# ---------
# Specifics
# ---------

if is_py2:
    from urllib3.packages.ordered_dict import OrderedDict  # noqa

    builtin_str = str
    bytes = str
    str = unicode  # noqa
    basestring = basestring  # noqa
    numeric_types = (int, long, float)  # noqa
    integer_types = (int, long)  # noqa

elif is_py3:
    from collections import OrderedDict  # noqa

    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int, float)
    integer_types = (int,)
