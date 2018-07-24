from abc import ABCMeta, abstractmethod, abstractclassmethod
from typing import Callable, Union, List, Tuple, Dict
import collections.abc
from functools import singledispatch

__all__ = ['Functor', 'fmap', 'Applicative', 'Monad', 'Monoid']


class Functor(metaclass=ABCMeta):
    @abstractmethod
    def fmap(self, f):
        """
        Returns TypeOfFunctor(f(self.data)),
        mimics fmap :: (a -> b) -> a -> b by
        fmap( fa ) -> type(fmap)(f(a))
        """
        pass


@singledispatch
def _fmap(fct, f):
    pass

FunctorB = Union[List, Tuple, Dict, Functor]

def fmap(f: Callable, fct: FunctorB) -> FunctorB:
    if isinstance(fct, Functor):
        return fct.fmap(f)
    if isinstance(fct, (list, tuple)):
        return type(fct)(map(f, fct))
    if isinstance(fct, dict):
        return {k: f(v) for k, v in fct.items()}


class Applicative(Functor, metaclass=ABCMeta):
    @abstractmethod
    def apply(self, x: Functor):
        pass

    def run(self):
        return self.fmap(lambda f: f())


class Monad(Applicative, metaclass=ABCMeta):
    @abstractmethod
    def __rshift__(self, f):
        pass


class Monoid(metaclass=ABCMeta):
    @abstractclassmethod
    def empty(self):
        pass

    @abstractmethod
    def __add__(self, x):
        pass

    @abstractclassmethod
    def concat(self, xs):
        pass
