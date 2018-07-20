# -*- coding: utf-8 -*-
import os
import sys
from contextlib import contextmanager

if os.name == 'nt':
    import win_unicode_console
    win_unicode_console.enable()


@contextmanager
def nocursor():
    if os.name == 'posix':
        try:
            sys.stdout.write('\033[?25l')   # hide cursor
            yield
        finally:
            print('finally')
            sys.stdout.write('\033[?25h')   # show cursor

    if os.name == 'nt':
        # import msvcrt
        import ctypes
        from ctypes import windll

        class _CursorInfo(ctypes.Structure):
            _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

        ci = _CursorInfo()
        handle = windll.kernel32.GetStdHandle(-11)
        windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))

        try:
            ci.visible = False
            windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
            yield
        finally:
            ci.visible = True
            windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))


class CLIProgress:
    fractions = ' ▏▎▍▌▋▊▉'
    full = '█'
    width = 40

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        with nocursor():
            for i in self.func(*args, **kwargs):
                length = i*self.width
                fulls = int(length)
                fraction_idx = int((length % 1)*8)

                sys.stdout.write('\033[K')  # clear to the end of the line
                print(self.full*fulls + self.fractions[fraction_idx], end='\r')


@CLIProgress
def progress(message):
    import time
    import numpy as np

    duration = 3
    ps = 100
    cycles = duration
    space = 0.5 + 0.5*np.sin(np.linspace(0, 2*np.pi*cycles, num=ps*duration))
    # space = np.linspace(0, 1, num=ps*duration)
    delay = 1/ps

    for i in space:
        time.sleep(delay)
        # print("%f: %s" % (i, message))
        yield i


if __name__ == '__main__':
    progress('asdf')
