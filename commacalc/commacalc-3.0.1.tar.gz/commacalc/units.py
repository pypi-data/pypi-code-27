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

import re
import math

from commacalc.extra import sign


_SYMBOLS = {
    'k': "1000",
    'M': "1000000",
    'G': "1000000000",
    'T': "1000000000000",
    'P': "1000000000000000",

    'm': "0.001",
    'μ': "0.000001",
    'n': "0.000000001",
    'p': "0.000000000001",
    'f': "0.000000000000001",

    '°': "(π/180)",
}


def replace_symbols(input_):
    """replace 123k with 1000*123"""
    for symbol, value in _SYMBOLS.items():
        input_ = re.sub(
            r'(\d+){}'.format(symbol),
            r'\1*{}'.format(value),
            input_
        )
    return input_


def from_fahrenheit(fahrenheit):
    """Convert Fahrenheits to Centigrade."""
    return (fahrenheit - 32)*5/9


C = from_fahrenheit


def to_fahrenheit(c):
    """Convert Centigrade to Fahrenheits."""
    return c*9/5 + 32


def prefix(x, dimension=1):
    """Give the number an appropriate SI prefix.

    :param x:   Too big or too small number.
    :returns:   String containing a number between 1 and 1000 and SI prefix.
    """
    if x == 0:
        return "0  "

    l = math.floor(math.log10(abs(x)))
    if abs(l) > 24:
        l = sign(l, value=24)

    div, mod = divmod(l, 3*dimension)
    # return "%.3g %s" % (x * 10**(-l + l % 3), " kMGTPEZYyzafpnµm"[l//3])
    return "{:.3g} {}".format(x*10**(-l + mod), " kMGTPEZYyzafpnµm"[div])


# maths
π = math.pi
φ = (1 + math.sqrt(5))/2


# time
days_in_year = 365.242189
seconds_in_day = 86400
seconds_in_year = days_in_year*seconds_in_day


# physics
c = 299792458
"""Speed of light in vacuum (exact) [ m s⁻¹ ]"""
G = 6.6738480e-11
"""Gravitational constant [ m³ kg⁻¹ s⁻² ]"""
h = 6.6260695729e-34
"""Planck constant [ m² kg s⁻¹ ]"""
ħ = h/(2*π)
"""Reduced Planck constant [ m² kg s⁻¹ ]"""
k_e = 8.9875517873681764e9
"""Coulomb constant (exact) [ m³ kg s⁻² C⁻² ]"""
k_B = 1.380648813e-23
"""Boltzmann constant [ m² kg K⁻¹ s⁻² ]"""

# eV = 1.60217656535e-19
eV = 1.602176620898e-19     # now
# eV = 1.602176634e-19        # future
"""Electronvolt [ m² kg s⁻² ]"""
q = eV
"""Elementary charge [ s A ]"""

µ_0 = 4*π*1e-7
"""Permeability of Vacuum (exact) [ kg m s⁻² A⁻² ]"""
ε_0 = 1/(µ_0*c**2)
"""Permittivity of Vacuum (exact) [ s⁴ A² kg⁻¹ m⁻³ ]"""
α = q**2/(4*π*ε_0*ħ*c)
"""Fine-structure constant [ ]"""


# astronomy
ly = 9460730472580800
"""Light-year (exact) [ m ]"""
au = 149597870700
"""Astronomical unit (exact) [ m ]"""
pc = 648000/π*au
"""Parsec (exact) [ m ]"""


# imperial units to metric (exact)
inch = 0.0254
foot = ft = 0.3048
yard = yd = 0.9144
mile = mi = 1609.344
acre = ac = 4046.8564224
pound = lb = 0.45359237
# imperial units to metric (not exact)
barrel = 0.15897
gallon_uk = 0.004546090
gallon_us = 0.003785412
ounce_int = oz = 0.028349523125
ounce_troy = toz = ozt = 0.0311034768


if __name__ == "__main__":
    print(prefix(0.9, 2))
