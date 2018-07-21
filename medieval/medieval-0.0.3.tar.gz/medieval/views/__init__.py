#!/usr/bin/env python
''' medieval.views
Displays army views and menu and general UI logic
'''

from contextlib import contextmanager
import curses
import curses.panel

SCREEN = None
WINDOW = None

@contextmanager
def start_view():
    init()
    try:
        yield
    finally:
        fini()

def init():
    global SCREEN, WINDOW
    SCREEN = curses.initscr()
    curses.noecho()
    curses.cbreak()
    SCREEN.keypad(1)
    height, width = SCREEN.getmaxyx()
    WINDOW = curses.newwin(height, width, 0, 0)

def fini():
    curses.nocbreak()
    SCREEN.keypad(0)
    curses.echo()
    curses.endwin()

def screen():
    return SCREEN

class Pad(object):
    
    def __init__(self, height=None, width=None):
        max_height, max_width = SCREEN.getmaxyx()
        height = height if height is not None else max_height
        width = width if width is not None else max_width
        self.height, self.width = height, width
        self.pad = curses.newpad(height, width)

    def center_text(self, text, height=None, mode=None):
        h, w = SCREEN.getmaxyx()
        if height is None:
            height = h / 2
        elif isinstance(height, float):
            height = int(h * height)
        height = min(h - 1, max(height, 0))
        width = w/2 - (len(text)/2)
        if mode is not None:
            self.pad.addstr(height, width, text, mode)
        else:
            self.pad.addstr(height, width, text)
        return height, width

    def addstr(self, *args, **kwargs):
        return self.pad.addstr(*args, **kwargs)
        
    def refresh(self, *args):
        return self.pad.refresh(*args)

    def addch(self, y, x, ch, mode=None):
        args = (y, x, ord(ch))
        if y + 1 == self.height and x + 1 == self.width:
            return
        if mode is not None:
            args += (mode,)
        return self.pad.addch(*args)

    def getch(self, *args):
        return self.pad.getch(*args)

    def pt(self, y, x):
        py, px = y, x
        if isinstance(y, float):
            py = int(self.height * y)
        if isinstance(x, float):
            px = int(self.width * x)
        return py, px

    @property
    def scr_height(self):
        return SCREEN.getmaxyx()[0]

    @property
    def scr_width(self):
        return SCREEN.getmaxyx()[1]


class Menu(object):
    
    def __init__(self, pos, options, title=None):
        y, x = pos
        height = len(options) + 1
        strings = zip(*options)[1]
        if title is not None:
            strings += (title,)
        width = max([len(s) for s in strings])
        self.win = curses.newwin(height, width, y, x)
        yoff = 0
        if title is not None:
            self.win.addstr(0, 0, title, curses.A_STANDOUT)
            yoff = 1
        for i, kv in enumerate(options):
            key, val = kv
            s = '{key}) {val}'.format(key=key, val=val)
            self.win.addstr(i + yoff, 0, s)
        self.win.refresh()
        self.val = None
        while True:
            c = self.win.getch()
            for key, val in options:
                if c == ord(key):
                    self.key = key
                    self.val = val
                    return
