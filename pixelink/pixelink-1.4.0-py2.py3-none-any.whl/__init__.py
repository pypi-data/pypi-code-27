""" Pixelink Camera driver package initializer. """

from .pixelink_api import PixeLINK
from .pixelink_api import PxLapi
from .pixelink_api import PxLerror
# from .pixelink_streamer import PxLstreamer

__all__ = ['PxLapi', 'PixeLINK', 'PxLerror']

__pkgname__ = 'pixelink'
__desc__ = 'A Python driver for the PixeLINK camera'
__created__ = '12/02/2014'
__updated__ = '31/07/2018'
__author__ = 'Hans Smit, Danny Smith'
__email__ = 'jcsmit@xs4all.nl, danny.smith@uq.edu.au'
__copyright_ = 'Copyright 2014 Hans Smit'
__license__ = 'GNU GPL'
__version__ = '1.4.0'
