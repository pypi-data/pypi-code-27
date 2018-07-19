from . import conflateddict


class MeanConflator(conflateddict.ConflatedDict):
    """
    ConflatedDict returning mean values.

    Example:
        >>> mc = MeanConflator()
        >>> mc['key'] = 1
        >>> mc['key'] = 2
        >>> mc['key'] = 3
        >>> print(mc['key'])
        2
        >>> c.reset()
        >>> mc['key'] = 5
        >>> print(mc['key'])
        5
    """

    def __init__(self):
        super(MeanConflator, self).__init__()
        self._raw = {}

    def __setitem__(self, key, data):
        """
        Update the mean value for key and mark key as dirty.
        """
        if not any((isinstance(data, int), isinstance(data, float))):
            raise TypeError('MeanConflator only supports numbers')

        val, count = self._raw.get(key, (0, 0))
        val += data
        count += 1
        self._raw[key] = (val, count)
        self._data[key] = val / count
        self._dirty.add(key)

    def additional_reset(self):
        """
        Resets the raw data to ensure a new mean is calculate for the next
        interval.
        """
        self._raw.clear()