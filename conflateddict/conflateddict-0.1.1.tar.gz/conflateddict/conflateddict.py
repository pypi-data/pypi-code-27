class ConflatedDict(object):
    """
    Simple ConflatedDict returning only dirty values

    Example:
        >>> import random
        >>>
        >>> keys = ['red', 'green', 'blue', 'orange']
        >>> con = ConflatedDict()
        >>> for _ in range(100):
        ...    con[random.choice(keys)] = random.randint(0, 100)
        ...
        >>> print(list(con.items())
        [('orange', 32), ('green', 71), ('red', 71), ('blue', 80)]
        >>> print(len(con))
        4
        >>> # After a reset, there will be no dirty values
        >>> con.reset()
        >>> print(list(con.items())
        []
        >>> print(len(con))
        0
        >>> # After another update, any new dirty values will be returned
        >>> con[random.choice(keys)] = random.randint(0, 100)
        >>> print(list(con.items())
        [('orange', 58)]
        >>>
        >>> # We still have access to all the values through data()
        >>> print(list(con.data().items()))
        [('blue', 80), ('red', 71), ('green', 71), ('orange', 58)]
        >>> print(len(con.data()))
        4
        >>>
    """

    def __init__(self):
        """
        Initialize ConflatedDict with empty dataset and no dirty keys.
        """
        self._data = {}
        self._dirty = set()

    def __str__(self):
        """
        Return description of the ConflatedDict
        """
        return (f'<{self.__class__.__name__} '
                f'dirty:{len(self._dirty)} entries:{len(self._data)}>')

    def __len__(self):
        """
        Return the number of dirty keys.
        """
        return len(self._dirty)

    def __iter__(self):
        """
        Return iterator over dirty keys.
        """
        return iter(self._dirty)

    def __setitem__(self, key, data):
        """
        Set (or update) the value of key to be equal to data and mark key
        as being dirty.
        """
        self._data[key] = data
        self._dirty.add(key)

    def __getitem__(self, key):
        """
        Return the stored value for key. Raises KeyError if key is not dirty.
        """
        if key in self._dirty:
            return self._data[key]
        raise KeyError(f'{key} not found in dirty set')

    def __contains__(self, key):
        """
        Return true if key is dirty.
        """
        return key in self._dirty

    def __delitem__(self, key):
        """
        Delete key and value from internal datastores. Raises KeyError
        if key is not dirty.
        """
        if key not in self._dirty:
            raise KeyError(key)
        self._dirty.remove(key)
        del self._data[key]

    def dirty(self, key):
        """
        Return True if the key is dirty.
        """
        return self.__contains__(key)

    def values(self):
        """
        Return iterator over dirty values.
        """
        for key in self._dirty:
            yield self._data[key]

    def keys(self):
        """
        Return iterator over dirty keys.
        """
        return iter(self._dirty)

    def items(self):
        """
        Return iterator over dirty (key, value) tuples.
        """
        for key in self._dirty:
            yield (key, self._data[key])

    def reset(self):
        """
        Resets dirty map. After calling this there will be no dirty keys.
        """
        self._dirty.clear()
        if hasattr(self, 'additional_reset'):
            self.additional_reset()

    def clear(self):
        """
        Clear out all the data in the ConflatedDict.
        """
        self._dirty.clear()
        self._data.clear()

    def data(self):
        """
        Return the complete datset.
        """
        return self._data
