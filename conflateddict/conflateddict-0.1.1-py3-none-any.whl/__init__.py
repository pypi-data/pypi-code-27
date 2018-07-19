"""
ConflatedDict

This module contains classes to assist with conflating streaming data. This can
be used to manage the load on consuming tasks, and is especially useful if the
consumers only need the current value and can thus safely discard intermediate
updates.

ConflatedDict - Basic ConflatedDict will only return the most recent value for
any key.

OHLCConflator - An ConflatedDict that will return the Open, High, Low, and
Close (last) values observed during the interval.

MeanConflator - A ConflatedDict that will return the mean of the values
observed during the interval. Values must be of type int or float.

BatchConflator - A ConflatedDict that will return all the values (in a batch)
observed during the interval.

LambdaConflator - A ConflatedDict that takes a user provided function of the
form f(v, vl) -> cv where v is the current value and vl is the list of past
values observed during the interval and returns the conflated value cv.

ModeConflator - A ConflatedDict that returns the mode (most common value) for
the key during the interval.
"""


__version__ = '0.1.1'

__author__ = 'Christian Reimer <christian.reimer@gmail.com>'

__all__ = ['ConflatedDict',
           'BatchConflator',
           'OHLCConflator',
           'MeanConflator',
           'LambdaConflator',
           'ModeConflator']


from .conflateddict import ConflatedDict
from .batchdict import BatchConflator
from .ohlcdict import OHLCConflator
from .meandict import MeanConflator
from .lambdadict import LambdaConflator
from .modedict import ModeConflator
