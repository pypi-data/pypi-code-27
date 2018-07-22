# @Author: Cameron Owens <cameron>
# @Date:   2018-07-17T16:26:45-05:00
# @Email:  cameronallanowens@gmail.com
# @Last modified by:   cameron
# @Last modified time: 2018-07-17T16:30:30-05:00



"""
Helper class definitions from the SubPackage Package
"""


class MySubClass1():
    def __init__(self):
        """
        Initializer method that takes no args
        """
        print("MySubClass1 initializer has been called")


    def addValues(self, value1,value2):
        return sum(value1, value2)


class MySubClass2():
    def __init__(self):
        """
        Initializer method that takes no args
        """
        print("MySubClass2 has been called")
