from . import conflateddict
import collections


ohlc = collections.namedtuple('ohlc', 'open high low close')


class OHLCConflator(conflateddict.ConflatedDict):
    """
    ConflatedDict returning Open, High, Low, and Close (Last) values.

    Example:
        >>> ohlc = OHLCConflator()
        >>> for i in [3, 1, 4, 1, 5, 9, 2]:
        ...     ohlc['key'] = i
        >>> print(ohlc['key'])
        ohlc(open=3, high=9, low=1, close=2)
    """

    def __init__(self):
        super(OHLCConflator, self).__init__()

    def __setitem__(self, key, data):
        """
        Set one or more of the Open, High, Low, Close values for key
        depending on the value of data. Close will always be updated.
        """
        _data = self._data.get(key, ohlc(data, data, data, data))

        if data > _data.high:
            # New high and new last
            self._data[key] = ohlc(_data.open, data, _data.low, data)
        elif data < _data.low:
            # New low and new last
            self._data[key] = ohlc(_data.open, _data.high, data, data)
        else:
            # New last
            self._data[key] = ohlc(_data.open, _data.high, _data.low, data)

        self._dirty.add(key)