# @Author: Cameron Owens <cameron>
# @Date:   2018-07-17T16:11:34-05:00
# @Email:  cameronallanowens@gmail.com
# @Last modified by:   cameron
# @Last modified time: 2018-07-17T16:47:47-05:00


"""
This is a basic class that is used in the package creation tutorial
"""

class MyFirstClass(object):
    def __init__(self, arg1=1, arg2=2):
        """
        Initializer method for the MyFirstClass object.

        Inputs: arg1 (int)
                arg2 (int)

        """
        self.arg1 = arg1
        self.arg2 = arg2


    def print_attributes(self):
        print("Your attributes are {attrs} and have values: {vals}".format(attrs=[self.__dict__.keys()], vals=self.__dict__.values()))
