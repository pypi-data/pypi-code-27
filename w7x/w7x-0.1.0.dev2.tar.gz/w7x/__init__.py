__version__ = '0.1.0.dev2'
__author__ = "Daniel Boeckenhoff"
__email__ = "daniel.boeckenhoff@ipp.mpg.de"

from . import lib
from .geo import GeoSet, getGeoSet
from .config import *
from . import core
from .core import is_w7x_instance, get_server, get_ws_class, run_service
from . import flt, vmec, extender
from .flt import MagneticConfig, Machine, Points3D
from .plotting.poincare import plot_poincare_surfaces, plot_poincare_geometries
