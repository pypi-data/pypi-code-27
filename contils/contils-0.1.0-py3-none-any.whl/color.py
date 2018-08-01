# coding=utf-8

import typing

from contils.raw import Raw

# reset         - \x1b[0m

# black         - \x1b[30m
# red           - \x1b[31m
# green         - \x1b[32m
# yellow        - \x1b[33m
# blue          - \x1b[34m
# magenta       - \x1b[35m
# cyan          - \x1b[36m
# light gray    - \x1b[37m

# gray          - \x1b[90m
# light red     - \x1b[91m
# light green   - \x1b[92m
# light yellow  - \x1b[93m
# light blue    - \x1b[94m
# light magenta - \x1b[95m
# light cyan    - \x1b[96m
# white         - \x1b[97m


class Color(Raw):
    _raw: typing.Any
    _color: str

    def __init__(self, raw: typing.Any, color: str):
        self._raw = raw
        self._color = color

    def __len__(self):
        return len(str(self._raw))

    def __str__(self):
        return f'{self._color}{self._raw}\x1b[0m'

    def __raw__(self) -> typing.Any:
        return self._raw

    def __format__(self, format_spec: str):
        result = ('{{0:{0}}}'.format(format_spec)).format(self._raw)

        return f'{self._color}{result}\x1b[0m'

    pass


def black(raw: typing.Any):
    return Color(raw, '\x1b[30m')


def red(raw: typing.Any):
    return Color(raw, '\x1b[31m')


def green(raw: typing.Any):
    return Color(raw, '\x1b[32m')


def yellow(raw: typing.Any):
    return Color(raw, '\x1b[33m')


def blue(raw: typing.Any):
    return Color(raw, '\x1b[34m')


def magenta(raw: typing.Any):
    return Color(raw, '\x1b[35m')


def cyan(raw: typing.Any):
    return Color(raw, '\x1b[36m')


def light_gray(raw: typing.Any):
    return Color(raw, '\x1b[37m')


def gray(raw: typing.Any):
    return Color(raw, '\x1b[90m')


def light_red(raw: typing.Any):
    return Color(raw, '\x1b[91m')


def light_green(raw: typing.Any):
    return Color(raw, '\x1b[92m')


def light_yellow(raw: typing.Any):
    return Color(raw, '\x1b[93m')


def light_blue(raw: typing.Any):
    return Color(raw, '\x1b[94m')


def light_magenta(raw: typing.Any):
    return Color(raw, '\x1b[95m')


def light_cyan(raw: typing.Any):
    return Color(raw, '\x1b[96m')


def white(raw: typing.Any):
    return Color(raw, '\x1b[97m')
