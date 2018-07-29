"""Custom Exceptions"""

import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class KissPackError(Exception):
    """Base exception for package"""
    pass
