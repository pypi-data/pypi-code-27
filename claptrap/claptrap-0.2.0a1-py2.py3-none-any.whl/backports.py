import abc
import bisect as _bisect
import itertools as _itertools
from random import random


### copypasta https://github.com/python/cpython/blob/16dfca4d8/Lib/random.py#L366
def choices(population, weights=None, *, cum_weights=None, k=1):
    """Return a k sized list of population elements chosen with replacement.
    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """
    # random = self.random
    n = len(population)
    if cum_weights is None:
        if weights is None:
            _int = int
            return [population[_int(random() * n)] for i in range(k)]
        cum_weights = list(_itertools.accumulate(weights))
    elif weights is not None:
        raise TypeError("Cannot specify both weights and cumulative weights")
    if len(cum_weights) != n:
        raise ValueError("The number of weights does not match the population")
    bisect = _bisect.bisect
    total = cum_weights[-1]
    hi = n - 1
    return [population[bisect(cum_weights, random() * total, 0, hi)] for i in range(k)]


### copypasta https://github.com/python/cpython/blob/16dfca4d8/Lib/_collections_abc.py#L72
def _check_methods(C, *methods):
    mro = C.__mro__
    for method in methods:
        for B in mro:
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True


### copypasta https://github.com/python/cpython/blob/16dfca4d8/Lib/contextlib.py#L15
class AbstractContextManager(metaclass=abc.ABCMeta):

    """An abstract base class for context managers."""

    def __enter__(self):
        """Return `self` upon entering the runtime context."""
        return self

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """Raise any exception triggered within the runtime context."""
        return None

    @classmethod
    def __subclasshook__(cls, C):
        if cls is AbstractContextManager:
            return _check_methods(C, "__enter__", "__exit__")
        return NotImplemented


### copypasta https://github.com/python/cpython/blob/16dfca4d8/Lib/contextlib.py#L342
class suppress(AbstractContextManager):
    """Context manager to suppress specified exceptions
    After the exception is suppressed, execution proceeds with the next
    statement following the with statement.
         with suppress(FileNotFoundError):
             os.remove(somefile)
         # Execution still resumes here if the file was already removed
    """

    def __init__(self, *exceptions):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exctype, excinst, exctb):
        # Unlike isinstance and issubclass, CPython exception handling
        # currently only looks at the concrete type hierarchy (ignoring
        # the instance and subclass checking hooks). While Guido considers
        # that a bug rather than a feature, it's a fairly hard one to fix
        # due to various internal implementation details. suppress provides
        # the simpler issubclass based semantics, rather than trying to
        # exactly reproduce the limitations of the CPython interpreter.
        #
        # See http://bugs.python.org/issue12029 for more details
        return exctype is not None and issubclass(exctype, self._exceptions)
