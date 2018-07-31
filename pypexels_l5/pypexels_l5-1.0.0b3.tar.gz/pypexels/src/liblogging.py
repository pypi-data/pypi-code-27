from __future__ import absolute_import

import logging

from .settings import LIB_NAME, LOG_LEVEL

logger = logging.getLogger(LIB_NAME)
logger.addHandler(logging.NullHandler())
logger.setLevel(LOG_LEVEL)
