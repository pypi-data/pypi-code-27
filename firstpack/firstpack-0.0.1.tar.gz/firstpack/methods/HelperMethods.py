# @Author: Cameron Owens <cameron>
# @Date:   2018-07-17T16:36:34-05:00
# @Email:  cameronallanowens@gmail.com
# @Last modified by:   cameron
# @Last modified time: 2018-07-17T16:45:54-05:00



"""
Helper Methods Module that demonstrates how to create methods for the use
within a package
"""

def HelperMethod1(arg1, arg2, banana):
    """
    Helper meethod for doing something cool. Exactly what it will do, we don't
    know that just yet.

    Inputs: arg1
            arg2
            banana #Because who doesn't like bananas?!?

    Outputs: A silly print statement
    """
    print("Method was called, did you call it? o_O")
    arguments = [arg1, arg2, banana]
    import random
    print("One day a {}, came into the office and was wearing a {} as a hat, thinking it was a {}".format(random.choice(arguments),random.choice(arguments),random.choice(arguments)))
