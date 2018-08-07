# -*- coding: utf-8 -*-

"""
version
"""

from __future__ import absolute_import

__all__ = ['__version__']

PACKAGE_NAME = 'hesong-ipsc-busnetcli'

try:
    from pkg_resources import get_distribution, DistributionNotFound
except ImportError:
    from ._version import version as __version__
else:
    try:
        __version__ = get_distribution(PACKAGE_NAME).version
    except DistributionNotFound:
        from ._version import version as __version__
