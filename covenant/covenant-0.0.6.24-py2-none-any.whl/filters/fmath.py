# -*- coding: utf-8 -*-
"""math filter"""

__author__  = "Adrien DELLE CAVE"
__license__ = """
    Copyright (C) 2018  doowan

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""

import logging
import math

from covenant.classes.filters import CovenantFilterBase, FILTERS

LOG = logging.getLogger('covenant.filters.math')


class CovenantMathFilter(CovenantFilterBase):
    FILTER_NAME = 'math'

    def init(self):
        funcs       = self.kwargs.pop('func')
        self._funcs = []

        if not isinstance(funcs, list):
            funcs = [funcs]

        for func in funcs:
            self._funcs.append(getattr(math, func))

        self._fargs         = list(self.kwargs.get('args', []) or [])
        self._value_arg_pos = int(self.kwargs.get('value_arg_pos') or 0)

    def run(self):
        fargs = list(self._fargs)
        fargs.insert(self._value_arg_pos, self.value)

        for func in self._funcs:
            fargs = [func(*fargs)]

        return fargs.pop(0)


if __name__ != "__main__":
    def _start():
        FILTERS.register(CovenantMathFilter)
    _start()
