from . import conflateddict
import collections


mode = collections.namedtuple('mode', 'value observations count')


class ModeConflator(conflateddict.ConflatedDict):
    """
    ConflatedDict returning the key value, the number of observations, and the
    total count. The key returned will be the one with the most observations
    in that interval (e.g. the mode). If there are multiple keys with the
    same mode, one of them will be returned.

    Example:
        >>> mc = ModeConflator()
        >>> mc['key'] = 1
        >>> mc['key'] = 2
        >>> mc['key'] = 2
        >>> mc['key'] = 2
        >>> mc['key'] = 2
        >>> mc['key'] = 3
        >>> print(mc['key'])
        mode(value=2, observations=4, count=6)
    """

    def __init__(self):
        super(ModeConflator, self).__init__()

    def __setitem__(self, key, data):
        """
        Update the mean value for key and mark key as dirty.
        """
        cnt = self._data.get(key, collections.Counter())
        cnt[data] += 1
        self._data[key] = cnt
        self._dirty.add(key)
    
    def __getitem__(self, key):
        """
        Return the most commonly observed value for key. Raises KeyError if
        key is not dirty.
        """
        if key in self._dirty:
            value, count = self._data[key].most_common(1)[0]
            return mode(value, count, sum(self._data[key].values()))
        raise KeyError(f'{key} not found in dirty set')
