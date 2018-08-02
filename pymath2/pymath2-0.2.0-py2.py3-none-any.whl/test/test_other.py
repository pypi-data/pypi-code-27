from pymath.other import *


def test_convert_base():
    assert convert_base(5, 2) == [1, 0, 1]
    assert convert_base(7, 4) == [1, 3]
