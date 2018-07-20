__version__ = '0.1.0.dev1'
__author__ = "Daniel Boeckenhoff"
__email__ = "daniel.boeckenhoff@ipp.mpg.de"

from .geo import GeoSet, getGeoSet
from .config import *
from . import core
from .core import is_w7x_instance, getServer, getWsClass, runService
from . import flt, vmec, extender
from .flt import MagneticConfig, Machine, Points3D
from .plotting.poincare import plot_poincare_surfaces, plot_poincare_geometries
