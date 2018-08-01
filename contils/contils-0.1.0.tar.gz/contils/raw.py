# coding=utf-8

import abc
import typing


class Raw(abc.ABC):
    @abc.abstractmethod
    def __raw__(self) -> typing.Any:
        pass

    pass
