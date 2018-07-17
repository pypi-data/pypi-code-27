from .susan import read_data, read_row_indices, has_row_indices
from .cooker import cook
from .forecaster import forecast
from .multip import *


__all__ = ['_Session']


class _Session(object):

    def __init__(self, data=None, row_indices=None):
        self.hist_data = data
        self.ready_data = None  # data after cook
        self.forecast_data = []
        self.row_indices = row_indices if row_indices else {}
        self.processes = 1  # number of processes

    def set_processes(self, n):
        assert isinstance(n, int) and n > 0, 'n must be positive integer!'
        self.processes = n

    def load_data(self, path, sep='\t', dtype=float):
        """ Load data and row indices.

        Note: All data elements are of the same data type.
        :param path: directory or single path or a list of paths
        :param sep: separator
        :param dtype: data type
        :return: iterable (each row of data)
        """
        self.hist_data = read_data(path, sep, dtype)
        if has_row_indices(path):
            i = 0
            for ri in read_row_indices(path):
                self.row_indices[ri] = i
                i += 1

    def cook_data(self, cooker_name, spices=None):
        """ Cook data.

        :param cooker_name: cooker name
        :param spices: single tuple or a list of tuples
        """
        self.ready_data = multi_process(cook, (self.hist_data, cooker_name, spices), self.processes)

    def forecast(self, forecaster_name, spices=None):
        """ Forecasts confidence intervals.

        :param forecaster_name: name of a registered forecaster
        :param spices: spices of forecaster
        """
        for item in multi_process(forecast, (self.ready_data, forecaster_name, spices), self.processes):
            self.forecast_data.append(item)
        return self.forecast_data

    def get_forecast_row(self, row_index):
        if isinstance(row_index, int):
            return self.forecast_data[row_index]
        else:
            return self.forecast_data[self.row_indices[row_index]]
