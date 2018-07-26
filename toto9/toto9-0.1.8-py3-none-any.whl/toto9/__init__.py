import logging
from pkg_resources import get_distribution

__version__ = get_distribution('toto9').version
__author__ = 'Nordstrom Cloud Engineering'
__email__ = 'cloudengineers@nordstrom.com'

import logging
from pkg_resources import get_distribution

class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logging.getLogger('toto9').addHandler(NullHandler())

__all__ = ['__version__']
