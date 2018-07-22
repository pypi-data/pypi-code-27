# @Author: Cameron Owens <cameron>
# @Date:   2018-07-17T17:05:38-05:00
# @Email:  cameronallanowens@gmail.com
# @Last modified by:   cameron
# @Last modified time: 2018-07-17T17:11:40-05:00



"""
Core level helper methods at the root of our package
"""


def BaseHelperMethod1(x,y):
    import math
    return(math.sqrt(x**2 + y**2))


def BaseHelperMethod2(string1, string2):
    """
    Method takes 2 strings, concatonates them and then changes their case
    """
    return string1.swapcase() + string2.swapcase()
