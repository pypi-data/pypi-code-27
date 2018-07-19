# Copyright (C) 2016  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import sys
import re
from math import *                      # noqa: F401, F403
import numbers

import commacalc.currencies
import commacalc.units
import commacalc.pretty_number

from commacalc.currencies import *      # noqa: F401, F403
from commacalc.units import *           # noqa: F401, F403
from commacalc.extra import *           # noqa: F401, F403
# from commacalc.primes import *


_FUNCTIONS = {
    '√': "sqrt",
    '∛': "cbrt",
}


def replace_functions(input_):
    """replace √123 or √(123) with sqrt(123)"""
    for symbol, value in _FUNCTIONS.items():
        input_ = re.sub(
            r'{}([\d.]+)'.format(symbol),
            r'{}(\1)'.format(value),
            input_
        )
    for symbol, value in _FUNCTIONS.items():
        input_ = re.sub(
            r'{}\('.format(symbol),
            r'{}('.format(value),
            input_
        )
    return input_


def main():
    input_ = ''.join(sys.argv[1:])

    input_ = replace_functions(input_)
    input_ = commacalc.currencies.replace_symbols(input_)
    input_ = commacalc.units.replace_symbols(input_)

    result = eval(input_)
    if isinstance(result, numbers.Real):
        result = commacalc.pretty_number.PrettyNumber(result)
    print(result)


if __name__ == '__main__':
    sys.argv = [',', '4*7']
    main()
