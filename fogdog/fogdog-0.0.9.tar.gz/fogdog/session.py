from ._session import *


__all__ = ['Session']


class Session(object):

    def __init__(self, data=None, row_indices=None):
        self._sess = _Session(data, row_indices)

    def set_processes(self, n):
        self._sess.set_processes(n)

    def load_data(self, path, sep='\t', dtype=int):
        """ cf. _Session.load_data
        """
        self._sess.load_data(path, sep, dtype)

    def cook_data(self, cooker, spices=None):
        """ cf. _Session.cook_data
        """
        self._sess.cook_data(cooker, spices)

    def forecast(self, forecaster, spices=None):
        """ cf. _Session.forecast
        """
        return self._sess.forecast(forecaster, spices)

    def get_forecast_row(self, row_index):
        return self._sess.get_forecast_row(row_index)

