"""All specific exception handling functions/clases used by multiple files"""
import multiprocessing as mp
import types
from .abstract import AbstractQueue

class is_queue(object):
    """raise an error if the queue isn't an instance of multiprocessing.Queue()"""

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        ret = self.f(*args, **kwargs)
        for arg in args[1:]:
            if not isinstance(arg, AbstractQueue):
                raise TypeError('queue must be an instance of an AbstractQueue')
        return ret

    def __get__(self, instance, objtype):
        types.MethodType(self, instance)


class is_int(object):
    """raise an error if the supplied type isn't an int."""

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        ret = self.f(*args, **kwargs)
        for arg in args[1:]:
            if not isinstance(arg, int):
                raise TypeError('{} is not an int'.format(arg))
        return ret

    def __get__(self, instance, objtype):
        return types.MethodType(self, instance)


class is_not_neg(object):
    """raise an error if the supplied type isn't an int."""

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        ret = self.f(*args, **kwargs)
        for arg in args[1:]:
            if arg < 0:
                raise ValueError('{} is must be greater than 1'.format(arg))
        return ret

    def __get__(self, instance, objtype):
        return types.MethodType(self, instance)


class check_end_time(object):
    """an error is raised if self._end_time is not set"""

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        if not args[0]._end_time:
            raise EndTimeNotSetError('end_time attribute hasn\'t been called yet')
        ret = self.f(*args, **kwargs)
        return ret

    def __get__(self, instance, objtype):
        return types.MethodType(self, instance)

class consumer_keys_set(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        if not args[0]._auth:
            raise ConsumerKeysNotSetError('call set_consumer_keys() first')
        ret = self.f(*args, **kwargs)
        return ret

    def __get__(self, instance, objtype):
        return types.MethodType(self, instance)


class ConsumerKeysNotSetError(Exception):
    """To be raised if consumer keys have not been set before access tokens"""

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)


class EndTimeNotSetError(Exception):
    """Raised if the end time hasn't been set prior to collecting tweets"""

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)
