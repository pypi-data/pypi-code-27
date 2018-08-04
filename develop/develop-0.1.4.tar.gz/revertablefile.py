# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

"""
Base class for working with text files on a line by line basis **and** global basis.

If you change the lines, set ._text to None, and .text will be re-generated from the .lines
on next access

If you change text, .lines is set to None automatically, and .lines will be re-generated
from the .text on next access

The original_text is kept
"""

from ruamel.std.pathlib import Path


class LineNotFound(Exception):
    pass


class MultipleLinesFound(Exception):
    pass


class RevertableFile:
    def __init__(self, file_name):
        try:
            self._file_name = file_name.resolve()
        except AttributeError:
            self._file_name = Path(file_name).resolve()
        self._lines = None
        self._text = None
        self._original_text = None

    @property
    def lines(self):
        if self._lines is None:
            self._lines = self.text.splitlines()
        return self._lines

    @property
    def text(self):
        if self._text is not None:
            return self._text
        if self._lines is not None:
            self._text = '\n'.join(self._lines) + '\n'  # EOF newline
            return self._text
        self._text = self.original_text
        return self._text

    @text.setter
    def text(self, val):
        # make sure the original is read in
        tmp = self.original_text  # NOQA
        self._text = val
        self._lines = None

    @property
    def original_text(self):
        if not self.has_been_read():
            self._original_text = self._file_name.read_text()
        return self._original_text

    def has_been_read(self):
        return self._original_text is not None

    def write(self):
        self._file_name.write_text(self.text)
        self._lines = None
