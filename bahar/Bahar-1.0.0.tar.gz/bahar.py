"""This is bahar.py module and it provides a function called count_vowels() that counts the number of vowels in a string. 
The purpose of writing this module is to practice preparing a python distribution."""

def count_vowels(the_string):
    """This function takes one argument called "the_string", which is any lowercase or uppercase string.
    The function returns the number of vowels in the string."""

    vowels = ['a', 'e', 'o', 'u', 'e', 'i']
    the_string = the_string.lower()
    count = 0
    for letter in the_string:
        if letter in vowels:
            count = count + 1
    print(the_string, 'has', count, 'vowels')