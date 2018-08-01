# coding=utf-8

import typing

from contils.raw import Raw


class Flash:
    def __init__(self):
        self._max_len = 0

    def print(self, msg: typing.Any):
        self.clear()
        self._max_len = max(self._max_len, len(str(msg.__raw__())) if isinstance(msg, Raw) else len(str(msg)))

        print(f'\r{msg}', end='')

    def clear(self):
        print('\r' + ' ' * self._max_len + '\r', end='')

    @staticmethod
    def end():
        print()

    pass
