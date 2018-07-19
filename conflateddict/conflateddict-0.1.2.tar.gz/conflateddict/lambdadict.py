from . import conflateddict


class LambdaConflator(conflateddict.ConflatedDict):
    """
    ConflatedDict which conflates based on a user provided function. The
    provided lambda must be of the format `lambda x, y: return z`

    Example:
        >>> lc = LambdaConflator(lambda x, y: x + sum(y))
        >>> lc['key'] = 1
        >>> lc['key'] = 2
        >>> print(lc['key'])
        3
        >>> lc['key] = 3
        6
    """

    def __init__(self, f_conf=lambda x, y: x, name=None):
        """
        Initialize LambdaConflator. The argument f_conf must be a function
        of the format `lambda x, y: return z` where x is the current value
        (when updating the conflator), y is the list of past values
        observed for this key (since the last reset), and z is the desired
        conflated value.
        """

        super(LambdaConflator, self).__init__()
        self._f_conf = f_conf
        self._raw = {}
        self._name = name

    def __setitem__(self, key, value):
        """
        Set value of key to be the result of calling the passed in conflator
        with value and the list of values previously observed for key. Also
        marks key as dirty.
        """
        _raw = self._raw.get(key, [])
        self._data[key] = self._f_conf(value, _raw)
        self._dirty.add(key)
        _raw.append(value)
        self._raw[key] = _raw

    def __str__(self):
        return f'<{self._name and self._name or self.__class__.__name__} ' \
            f'dirty:{len(self._dirty)} entries:{len(self._data)}>'

    def additional_reset(self):
        """
        Resets the raw data to ensure a new mean is calculate for the next
        interval.
        """
        self._raw.clear()