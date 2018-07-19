from . import conflateddict

class BatchConflator(conflateddict.ConflatedDict):
    """
    ConflatedDict that batches values together.

    Example:
        >>> bc = BatchConflator()
        >>> for c in 'red green blue orange'.split():
        ...     bc['colors'] = c
        >>> for n in range(5):
        ...     bc['num'] = n
        >>> print(bc['colors'])
        ['red', 'green', 'blue', 'orange']
    """

    def __init__(self):
        super(BatchConflator, self).__init__()

    def __setitem__(self, key, data):
        """
        Append data to the batch of values for key and mark key as dirty.
        """
        if key not in self._dirty:
            # This is the first time (in this interval) that we see this key,
            # so we need to clear out the data for this key
            _data = []
        else:
            _data = self._data[key]

        _data.append(data)
        self._data[key] = _data
        self._dirty.add(key)