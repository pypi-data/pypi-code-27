# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals


"""
Work with project README information: README.rst, CHANGES

The idea is that this information is only read once, but can be updated
and written multiple times.

Although these files are normally under revision control, they are not that big
and revert information (the original read file content) are kept and can be
written out.

"""

from .revertablefile import RevertableFile, LineNotFound, MultipleLinesFound


class ReadMe(RevertableFile):
    def find_single_line_starting_with(self, val, raise_on_error=True):
        res = []
        for idx, line in enumerate(self.lines):
            if line.startswith(val):
                res.append(idx)
        if len(res) == 1:
            return res[0]
        if not raise_on_error:
            return None
        if len(res) > 0:
            raise MultipleLinesFound(f'\n  too many lines found starting with [{val}]: {res}')
        assert len(res) == 0
        raise LineNotFound(f'no line found starting with [{val}]')
