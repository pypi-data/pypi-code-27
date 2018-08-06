"""
Author: qiacai
"""

from collections import OrderedDict
from schematics.exceptions import ConversionError, BaseError, CompoundError
from collections import Mapping

from ada_core.data_model.entry import Entry


class TimeSeries(OrderedDict):

    def __init__(self, data: dict = None):
        super(TimeSeries, self).__init__()

        if data is not None:
            self.load_data(data)

    @property
    def start(self):
        """
        Return the earliest timestamp in the ts
        :return: int
        """
        return min(self.keys()) if self.keys() else None

    @property
    def end(self):
        """
        Return the latest timestamp in the ts
        :return: int
        """
        return max(self.keys()) if self.keys() else None

    def __repr__(self):
        return 'TimeSeries<start={0}, end={1}>'.format(repr(self.start), repr(self.end))

    def __str__(self):
        """
        :return string: Return string representation of time series
        """
        string_rep = ''
        for item in self.items():
            if not string_rep:
                string_rep += str(item)
            else:
                string_rep += ', ' + str(item)
        return 'TimeSeries([{}])'.format(string_rep)

    def getEntryList(self):
        entryList = []
        for key, value in self.items():
            entryList.append(Entry(key, value))
        return entryList

    def getValueList(self):
        return list(self.values())

    def getKeyList(self):
        return list(self.keys())

    def popEntry(self, key=None):
        if key is None:
            key = max(self.keys())
        entry = Entry(key, self.get(key))
        self.pop(key)
        return entry

    def split(self, key, direct=False):
        if key < 0 or key > max(self.keys()):
            return TimeSeries()

        ret_ts = {}
        keyList = list(self.keys())
        keyList = [keya for keya in keyList if keya>=key]
        for keya in keyList:
            ret_ts.update({keya:self.get(keya)})
            if direct:
                self.pop(keya)
        return TimeSeries(ret_ts)

    def load_data(self, value):

        if not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used to load TimeSeries')

        errors = {}
        for k in sorted(value.keys()):
            try:
                self.update({int(k): float(value.get(k))})
            except (BaseError, ValueError) as exc:
                errors[k] = exc
        if errors:
            raise CompoundError(errors)