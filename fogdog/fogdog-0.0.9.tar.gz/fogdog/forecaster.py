import numpy as np
import scipy.stats as ss
from .logger import logger


__all__ = ['forecaster']


# --------------------------------
# Decorator
# For registering forecasters
# --------------------------------
class Forecaster(object):

    def __init__(self):
        self._forecasters = {}

    def __call__(self, name):
        if not self._is_name_valid(name):
            raise ValueError('forecaster name already exists! name = %s' % name)

        def wrapper(func):
            self._forecasters[name] = func
            return func
        return wrapper

    def _is_name_valid(self, name):
        if name in self._forecasters.keys():
            return False
        return True

    def getattr(self, name):
        if name in self._forecasters.keys():
            return self._forecasters[name]
        else:
            raise ValueError('Forecaster is not registered! name = %s' % name)


forecaster = Forecaster()
# --------------------------------


def forecast(data, forecaster_name, spices=None):
    """ Forecasts confidence intervals.

    :param data: Iterable rows
    :param forecaster_name: name of a registered forecaster
    :param spices: spices of the forecaster
    :return: list
    """
    logger.info("Forecaster: %s" % forecaster_name)
    if not spices:
        spices = ()
    if not isinstance(spices, tuple):
        raise ValueError('spices must be tuple!')

    return [forecaster.getattr(forecaster_name)(row, *spices) for row in data]


# --------------------------------
# Registered forecasters.
# --------------------------------

@forecaster('LR')
def lr(row, fn=1, alpha=50):
    """ Forecasting confidence interval under Normal distribution.

    :param row: 1d array or list
    :param alpha: percentage confidence level
    :param fn: the number of forecasting time units
    :return: list
    """

    x = np.array(range(len(row)))
    # linear regression
    slope, intercept, r_value, p_value, std_err = ss.linregress(x, row)
    # forecast
    res = []
    for i in range(fn):
        mean = slope * (len(x) + fn) + intercept
        res.append(ss.norm.interval(alpha / 100, mean, std_err))
    return res

