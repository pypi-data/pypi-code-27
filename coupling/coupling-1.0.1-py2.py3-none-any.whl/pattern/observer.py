# -*- coding: utf-8 -*-

import threading
from abc import ABCMeta, abstractmethod

import logging
logger = logging.getLogger(__name__)


class BaseObservable:
    def __init__(self):
        self._observers = []
        self.lock = threading.Lock()

    def __getstate__(self):
        excludes = ("lock", )
        state = {k: v for k, v in self.__dict__.items() if k not in excludes}
        return state

    def __setstate__(self, state):
        self._observers = state["_observers"]
        self.lock = threading.Lock()

    def notify(self, *args, **kwargs):
        with self.lock:
            for observer in self._observers:
                observer.update(self)

    def attach(self, observer: "BaseObserver") -> None:
        with self.lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def detach(self, observer: "BaseObserver") -> None:
        with self.lock:
            if observer in self._observers:
                self._observers.remove(observer)


class BaseObserver(metaclass=ABCMeta):
    @abstractmethod
    def update(self, observable: BaseObservable) -> None:
        pass
