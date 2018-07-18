import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

from base import Base
from client_proxy import Proxy

__version__ = '0.0.4'
