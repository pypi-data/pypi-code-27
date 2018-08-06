# coding=utf-8
""" This module contains special functionality related to terminal output.
    It implements a simple command line GUI for the esahub package.
"""
from __future__ import print_function
from .config import CONFIG
# import struct
import sys
import time
import curses
import multiprocessing
from threading import Timer


def init():
    Screen.start()


def quit():
    Screen.quit()


def progressBar(progress, total, prefix='', suffix='', length=30, fill='#'):
    """Returns the string representation of a progress bar with `progress`
    filled.

    Parameters
    ----------
    progress : int
    total : int
    prefix : str, optional
    suffix : str, optional
    length : int, optional
        The length of the progress bar (default: 30)
    fill : char, optional
        The character constituting the progress bar (default: '#')

    Returns
    -------
    str
        A string representation of the progress bar.
    """
    if total == 0:
        fraction = 1.0
    else:
        fraction = min(1.0, progress/float(total))
    percent = ('{:5.0f}').format(100.0 * fraction)
    filledLength = int(length * fraction)
    bar = fill * filledLength + ' ' * (length - filledLength)
    return '{}[{}] {}%{}'.format(prefix, bar, percent, suffix)


class Screen:
    """A custom Screen class representing the GUI.
    """
    INITIATED = False
    LINE_COUNT = 0
    REFRESH_INTERVAL = 0.3
    CONTENT_START = 3
    CONTENT = []
    CONTENT_DICT = {}
    LAST_REFRESHED = time.time()
    WINDOW = None
    HEIGHT = 0
    WIDTH = 0
    LINES = 0
    TITLE = ''
    STATUS = ''
    PROGRESS = (0, 1)
    RESULT = ''
    PROMPT = ''
    SCROLL_POS = 0
    MAX_CONTENT_LENGTH = 0

    @classmethod
    def start(cls):
        """Start curses application."""
        cls.WINDOW = curses.initscr()
        cls.INITIATED = True
        cls.HEIGHT, cls.WIDTH = cls.WINDOW.getmaxyx()
        cls.LINES = cls.HEIGHT - cls.CONTENT_START - 4

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        cls.WINDOW.keypad(1)
        cls.WINDOW.idcok(False)
        cls.WINDOW.idlok(False)

        # Set color schemes
        # curses.start_color()
        # curses.init_pair(RED_ON_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)

        cls.WINDOW.refresh()

        # REDRAW SCREEN EVERY `REFRESH_INTERVAL` SECONDS
        cls.time_refresh()

    @classmethod
    def time_refresh(cls):
        def wrapper():
            cls.time_refresh()
            cls.redraw()
        if cls.INITIATED:
            t = Timer(cls.REFRESH_INTERVAL, wrapper)
            t.start()
            return t
        else:
            return False

    @classmethod
    def paint(cls):
        """Paint the full GUI without explicity clearing the screen."""
        if cls.INITIATED:
            cls.HEIGHT, cls.WIDTH = cls.WINDOW.getmaxyx()
            cls.LINES = cls.HEIGHT - cls.CONTENT_START - 4

            cls.WINDOW.move(0, 0)
            # cls.WINDOW.refresh()

            cls.redraw_content()

            # Print title
            cls.set_header(cls.TITLE, force=True)
            # Print status
            cls.print_status_line()
            # Print result
            cls.set_result(cls.RESULT, force=True)
            # Print prompt
            cls.set_prompt(cls.PROMPT, force=True)

            cls.WINDOW.refresh()

    @classmethod
    def redraw_content(cls):
        """Draw the content lines from buffer."""
        if cls.INITIATED:

            # Print only lines from SCROLL_POS to SCROLL_POS + LINES
            counter = 0
            for pos, line in enumerate(
                cls.CONTENT[cls.SCROLL_POS:cls.SCROLL_POS+cls.LINES]
            ):
                cls.__print_line(cls.CONTENT_START+pos, line)
                counter += 1

            if counter < cls.LINES:
                for pos in range(counter, cls.LINES):
                    cls.__clear_line(cls.CONTENT_START+pos)

            cut_above = cls.SCROLL_POS
            cut_below = len(cls.CONTENT) - cls.LINES - cls.SCROLL_POS
            if cut_above > 0:
                cls.__print_line(2, '... {} more (press arrow up)'
                                    .format(cut_above))
            else:
                cls.__clear_line(2)
            if cut_below > 0:
                cls.__print_line(cls.HEIGHT-4, '... {} more (press arrow down)'
                                               .format(cut_below))
            else:
                cls.__clear_line(cls.HEIGHT-4)

            cls.WINDOW.refresh()

    @classmethod
    def redraw(cls):
        """Fully erase and redraw the GUI from the buffer."""
        if cls.INITIATED:
            lock = multiprocessing.Lock()
            lock.acquire()
            cls.WINDOW.erase()
            curses.doupdate()
            cls.paint()
            lock.release()

    @classmethod
    def update(cls, key, text):
        """Update the specified piece of content.

        Content is stored as a key-value pair, allowing to update the status
        for each line easily. Appends a new key if it does not yet exist.

        Parameters
        ----------
        key : str
        text : str
        """
        cls.MAX_CONTENT_LENGTH = max(cls.MAX_CONTENT_LENGTH, len(text))
        if key in cls.CONTENT_DICT:
            cls.set_line(cls.CONTENT_DICT[key], text)
        else:
            pos = cls.append(text)
            cls.CONTENT_DICT[key] = pos

    @classmethod
    def set_line(cls, pos, line, force=False):
        """Update a specific line."""
        lock = multiprocessing.Lock()
        lock.acquire()
        try:
            # Too short: add empty lines...
            while len(cls.CONTENT) <= pos:
                cls.CONTENT.append('')

            # print('CONTENT[{}] = {}'.format(pos,line), file=sys.stderr)
            cls.CONTENT[pos] = line

            if force:
                cls.redraw()
            # else:
            #     cls.time_refresh()

        finally:
            lock.release()

    @classmethod
    def append(cls, text):
        pos = len(cls.CONTENT)
        cls.set_line(pos, text)
        # cls.set_result('Now {} lines in CONTENT'.format(pos))

        if len(cls.CONTENT) - cls.SCROLL_POS > cls.LINES:
            cls.scroll_down()

        return pos

    @classmethod
    def __print_line(cls, pos, text, fmt=0, right=''):
        if cls.INITIATED:
            # lock = multiprocessing.Lock()
            # lock.acquire()
            try:
                # text = '{:3d}_{}'.format(pos,text)
                text = ' '+text
                right = right+' '
                prefix = '...'

                if cls.CONTENT_START <= pos < cls.CONTENT_START + cls.LINES:
                    # This is a content body line!
                    space = cls.WIDTH - cls.MAX_CONTENT_LENGTH - 2
                    if space >= 0:
                        text = text.ljust(cls.WIDTH)
                    else:
                        startpos = len(prefix) - space
                        text = (prefix + text[startpos:]).ljust(cls.WIDTH)
                else:
                    # This is a header or footer line!
                    space = cls.WIDTH - len(text) - len(right)
                    if space >= 0:
                        text = text + ' '*space + right
                    else:
                        startpos = len(prefix) - space
                        text = prefix + text[startpos:] + right

                # Make sure to only print in allowed area.
                if 0 <= pos < cls.HEIGHT:
                    try:
                        cls.WINDOW.move(0, 0)
                        # cls.WINDOW.refresh()
                        cls.WINDOW.addstr(pos, 0, text, fmt)
                        # cls.WINDOW.refresh()
                    except:
                        # print('pos={},text={},fmt={}'.format(pos,text,fmt),
                        # file=sys.stderr)
                        raise

            finally:
                # lock.release()
                pass

    @classmethod
    def __clear_line(cls, pos):
        if cls.INITIATED:
            cls.WINDOW.move(0, 0)
            # cls.WINDOW.refresh()
            cls.WINDOW.addstr(pos, 0, ' '*cls.WIDTH, 0)
            # cls.WINDOW.refresh()

    @classmethod
    def scroll_up(cls, lines=1):
        if cls.SCROLL_POS > 0:
            cls.SCROLL_POS -= lines
        else:
            cls.SCROLL_POS = 0
        cls.redraw_content()

    @classmethod
    def scroll_down(cls, lines=1):
        if len(cls.CONTENT) - cls.SCROLL_POS > cls.LINES:
            cls.SCROLL_POS += lines
        else:
            cls.SCROLL_POS = len(cls.CONTENT) - cls.LINES
        cls.redraw_content()

    @classmethod
    def print_status_line(cls):
        if cls.INITIATED:
            text = 'STATUS: ' + cls.STATUS
            if cls.PROGRESS is None:
                cls.__print_line(1, text, fmt=curses.A_REVERSE)
            else:
                cls.__print_line(1, text, fmt=curses.A_REVERSE,
                                 right=progressBar(*cls.PROGRESS))
        elif sys.stdout.isatty():
            if cls.PROGRESS is None:
                print('\r{}'.format(cls.STATUS), end='')
            else:
                print('\r{} {}'.format(cls.STATUS, progressBar(*cls.PROGRESS)),
                      end='')
            sys.stdout.flush()

    @classmethod
    def set_header(cls, text, force=True):
        cls.TITLE = text
        if force:
            cls.__print_line(0, cls.TITLE)

    @classmethod
    def set_status(cls, text, progress=None, force=True):
        cls.STATUS = text
        cls.PROGRESS = progress
        if force:
            cls.print_status_line()

    @classmethod
    def set_progress(cls, progress, total, force=True):
        cls.PROGRESS = (progress, total)
        if force:
            cls.print_status_line()

    @classmethod
    def set_result(cls, text, force=True):
        cls.RESULT = text
        if not cls.INITIATED and sys.stdout.isatty():
            print(cls.RESULT)
        elif force:
            cls.__print_line(cls.HEIGHT-3, cls.RESULT, fmt=curses.A_REVERSE)

    @classmethod
    def set_prompt(cls, text, force=True):
        cls.PROMPT = text
        if force:
            cls.__print_line(cls.HEIGHT-2, cls.PROMPT)

    @classmethod
    def wait_for_quit(cls):
        if cls.INITIATED:
            cls.redraw()
            cls.set_prompt('Press q to exit...')
            while 1:
                c = cls.WINDOW.getch()
                if c == curses.KEY_RESIZE:
                    cls.redraw()
                if c == ord('q'):
                    break
                elif c == curses.KEY_UP:
                    cls.scroll_up()
                elif c == curses.KEY_DOWN:
                    cls.scroll_down()
                elif c == curses.KEY_PPAGE:
                    cls.scroll_up(cls.LINES)
                elif c == curses.KEY_NPAGE:
                    cls.scroll_down(cls.LINES)
            cls.quit()

    @classmethod
    def quit(cls):
        """End curses application."""
        if cls.INITIATED:
            curses.nocbreak()
            curses.echo()
            curses.curs_set(1)
            curses.endwin()
            cls.INITIATED = False


# -----------------------------------------------------------------------------
def redraw():
    Screen.redraw()


def wait_for_quit():
    Screen.wait_for_quit()


def append(text):
    return Screen.append(text)


def update(key, text):
    return Screen.update(key, text)


# def separator(line):
#     printline(line, '='*Screen.WIDTH)


def header(text):
    Screen.set_header(text)


def status(text, progress=None):
    Screen.set_status(text, progress=progress)


def finish_status():
    if not Screen.INITIATED:
        print('')


def result(text):
    Screen.set_result(text)


def prompt(text):
    Screen.set_prompt(text)


def set_progress(progress, total, force=True):
    Screen.set_progress(progress, total, force=force)


# TERMINAL OUTPUT FORMATTING
# -----------------------------------------------------------------------------
PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


def error(message):
    if False and sys.stdout.isatty() and not CONFIG['GENERAL']['USE_GUI']:
        return '{0}{1}{2}{3}'.format(BOLD, RED, message, END)
    else:
        return message


def warn(message):
    if False and sys.stdout.isatty() and not CONFIG['GENERAL']['USE_GUI']:
        return '{0}{1}{2}{3}'.format(BOLD, YELLOW, message, END)
    else:
        return message


def success(message):
    if False and sys.stdout.isatty() and not CONFIG['GENERAL']['USE_GUI']:
        return '{0}{1}{2}{3}'.format(BOLD, GREEN, message, END)
    else:
        return message
