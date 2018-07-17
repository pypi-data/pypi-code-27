import logging
from json import JSONEncoder
import warnings
import numpy


class MissingLinkJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, (numpy.ndarray, numpy.matrix)):
            return obj.tolist()
        elif type(obj).__name__ == type.__name__:
            return obj.__name__

        try:
            return super(MissingLinkJsonEncoder, self).default(obj)
        except TypeError:
            with warnings.catch_warnings():
                warnings.simplefilter("once")
                warnings.warn("skipped MissingLinkJsonEncoder because of TypeError")
            return None
