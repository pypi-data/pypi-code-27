import random
import os


def extract_random_line_from_file(file):
    if random.randint(1, 2) % 2 == 0:
        my_path = os.path.abspath(os.path.dirname(__file__))
        file = os.path.join(my_path, 'files/adjectives.txt')
    else:

        my_path = os.path.abspath(os.path.dirname(__file__))
        file = os.path.join(my_path, 'files/nouns.txt')

    open_file = open(file, "r")
    lines = open_file.readlines()
    """
    This function has an efficient memory usage because instead of storing in a list I simply return a random line from 
    the file. More memory efficient at the cost of execution speed.
    from the file.The strip() method is used to remove the \n newline character that each line might have. 
    
    """
    return lines[random.randint(0, len(lines) - 1)].strip().lower()


"""
.option('-w, --words [num]', 'number of words [2]', 2)
    .option('-n, --numbers', 'use numbers')
    .option('-a, --alliterative', 'use alliterative')
    .option('-o, --output [output]', 'output type [raw|dashed|spaced]', /^(raw|dashed|spaced)$/i)

"""


def concatenate_words(number, join_char):
    return join_char.join([extract_random_line_from_file(file='files/adjectives.txt') for i in range(0, number)])


def add_postfix(string, separation_char, postfix):
    return string + str(separation_char) + str(postfix)


def add_prefix(prefix, string, separation_char):
    return str(prefix) + str(separation_char) + string


