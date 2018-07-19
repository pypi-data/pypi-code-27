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

class Pattern:
    def __new__(cls, pattern=None, **kwargs):
        """
        >>> a = Pattern()
        >>> b = Pattern(a)
        >>> a is b
        True
        """
        if pattern.__class__ is cls:
            return pattern
        return super(Pattern, cls).__new__(cls)

    regex = type_ = preceded_by = child_of = descendand_of = None

    def __init__(self, pattern=None,
                 preceded_by=None, child_of=None, descendand_of=None):
        """
        >>> from nodes import *
        >>> pattern = RoundNode > ".*bbb.*" + DoubleQNode
        >>> pattern.type_
        <class 'nodes.DoubleQNode'>
        >>> pattern.preceded_by.regex
        '.*bbb.*'
        >>> pattern.child_of.type_
        <class 'nodes.RoundNode'>
        """
        if pattern.__class__ is Pattern:
            pass
        elif isinstance(pattern, str):
            self.regex = pattern
            self.type_ = None
        else:
            self.regex = None
            self.type_ = pattern

        if preceded_by:
            self.preceded_by = preceded_by
        if child_of:
            self.child_of = child_of
        if descendand_of:
            self.descendand_of = descendand_of

    def __add__(cls, other):
        return Pattern(other, preceded_by=Pattern(cls))

    # def __radd__(cls, other):
    #     return Pattern(cls, preceded_by=Pattern(other))

    def __gt__(cls, other):
        return Pattern(other, child_of=Pattern(cls))

    # def __lt__(cls, other):
    #     return Pattern(cls, child_of=Pattern(other))

    def __lshift__(cls, other):
        return Pattern(other, descendand_of=Pattern(cls))

    # def __rshift__(cls, other):
    #     return Pattern(cls, descendand_of=Pattern(other))


class PatternType(type, Pattern):
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
