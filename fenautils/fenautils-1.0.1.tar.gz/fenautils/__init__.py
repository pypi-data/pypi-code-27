import os
import re
import errno
import codecs

SEMANTIC_VERSION = "1.0.1"

"""
Simple assert utils to make sure that an object matches some specified type
or the items in an iterable match some specified type

The main difference between using this function and using assert isinstance(...)
is that it provides a more in-depth error message

Running unit testing: `python3 -m unittest discover -s unittests`
"""

def assert_type(checked_object, *valid_types, additional_message=None, optional=False):
    """
    Checks whether an object is an instance of any of the valid types

    Args:
        checked_object (any)
        valid_types (any)
        additional_message (str or None)
        optional (bool): Whether the object can be a None object or not
    """
    assert isinstance(additional_message, str) or additional_message is None
    assert isinstance(optional, bool)

    if not (isinstance(checked_object, valid_types) or (optional and checked_object is None)):
        if len(valid_types) == 1:
            checked_types_str = f"{valid_types[0]}"
        else:
            checked_types_str = f"one of {valid_types}"

        if optional:
            checked_types_str += " or None"

        full_message = f"Expected type of {checked_object!r} to be {checked_types_str} but got {type(checked_object)}"
        #full_message = f"Expected type of {type(checked_object)} to be {checked_types_str} but got {type(checked_object)}"
        if additional_message is not None:
            full_message += f" {additional_message}"
        raise AssertionError(full_message)

def assert_iterable_types(checked_iterable, *valid_types, duplicate_key=None):
    """
    Checks whether all objects in a iterable are instances of one of the valid types

    Args:
        checked_iterable (iterable)
        valid_types (any)
        duplicate_key (None or callable): A function to give the value to check for duplicates
            Note that if you want to detect duplicates with itself, just do `duplicate_key=lambda x: x`
            If the option is None, no duplicate checking will be done

    """
    for index, item in enumerate(checked_iterable):
        assert_type(item, *valid_types, additional_message=f"in index {index} of iterable {checked_iterable}")

    # checks for duplicates
    if duplicate_key is not None:
        assert callable(duplicate_key), "The duplicate key must be a function"

        # uses a set because only the containment of an item matters
        found_objects = set()

        # iterates through each checked object to see if its within the found objects
        for checked_object in checked_iterable:
            result_object = duplicate_key(checked_object)
            # assert result_object not in found_objects, f"Found a duplicate of {result_object!r} in iterable {checked_iterable}"
            assert result_object not in found_objects, f"Found a duplicate of {result_object!r} in {checked_object!r}"
            found_objects.add(result_object)

def assert_list_types(checked_list, *valid_types, **kwargs):
    assert_type(checked_list, list)
    assert_iterable_types(checked_list, *valid_types, **kwargs)

def assert_tuple_types(checked_tuple, *valid_types, **kwargs):
    assert_type(checked_tuple, tuple)
    assert_iterable_types(checked_tuple, *valid_types, **kwargs)

"""
Utils to change the message of an exception
"""

__all__ = [
    "exc_add_msg",
    "exc_set_msg",
    ]

def exc_add_msg(e: Exception, message: str, sep=" "):
    """
    Args:
        e (Exception): The exception to add a message to
        message (str): The message to be added to the exception
    """

    args = list(e.args)
    assert args, "You can only add a message if a message exists"
    args[-1] += sep + message
    e.args = tuple(args)


def exc_set_msg(e: Exception, message: str):
    """
    Args:
        e (Exception): The exception to set a message to
        message (str): The message to be set to the exception
    """
    e.args = (message,)


def make_dirs(file_path):
    """
    Makes the directories if the directories to the file path does not exist

    Args:
        file_path (str): the path-like object to the file

    Answer comes from:
        https://stackoverflow.com/a/12517490
    """
    dir_path = os.path.realpath(os.path.dirname(file_path))
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as e: # Guard against race condition
            if e.errno != errno.EEXIST:
                raise



_alpha = re.compile("[A-Za-z_]")
_json_number = re.compile(r"-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?")
_nbt_float = re.compile(r"-?(0|[1-9]\d*)(\.\d+)([eE][+-]?\d+)?")

def is_json_number(string):
    """
    json_number ::= ("-")? && INT && ("." && INT)? && (["e", "E"] && ["+", "-"] && INT)?
    Follwing the picture for a general json number:
        http://www.json.org/number.gif
    """
    return bool(re.fullmatch(_json_number, string))

def is_number(string):
    """
    Checks whether the string has a proper signed number format for minecraft

    Args:
        string

    Returns:
        bool
    """

    try:
        float(string)
    except ValueError:
        return False

    # checks whether there is an alphabetical value is inside the number
    if re.search(_alpha, string) is not None:
        return False
    return True

def is_signed_int(num_str):
    """
    Args:
        num_str (str): The string that is checked to see if it represents a number

    Returns:
        bool
    """
    # if the num_str is a digit, that means that there are no special characters within the num_str
    # therefore making it a nonneg int
    # to check if it is a signed integer, the string is checked for one "-" and then the rest being the format of a nonneg int

    assert isinstance(num_str, str)
    return num_str.isdigit() or (num_str.startswith("-") and num_str[1:].isdigit())

def is_nonneg_int(num_str):
    """
    Args:
        num_str (str): The string that is checked to see if it represents a nonneg integer

    Returns:
        bool
    """

    assert isinstance(num_str, str)
    return num_str.isdigit()

def is_pos_int(num_str):
    """
    Args:
        num_str (str): The string that is checked to see if it represents a positive integer (not 0)

    Returns:
        bool
    """

    assert isinstance(num_str, str)
    if num_str.isdigit():
        return int(num_str) != 0
    return False


"""
http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html
http://jfine-python-classes.readthedocs.io/en/latest/decorators.html

Syntax of a decorator on a class:
    @decorator
    class A:
        ...
    a = A()

is equal to
    class A:
        ...
    a = decorator(A)
"""

def addrepr(cls):
    """
    Decorator meant to be used on classes to set a __repr__ method
    that contains all variables of the classes
    """
    def __repr__(self):
        # `type(self)` is used instead of `cls` because `cls` only refers to the most parent object if inherited
        # while `type(self)` guarantees to get the class name of the current class
        class_name = type(self).__name__

        variables = []
        for variable, value in vars(self).items():
            variables.append(f"{variable}={value!r}")
        variables_str = ", ".join(variables)

        return f"{class_name}[{variables_str}]"

    # sets the __repr__ method as the defined __repr__ because methods can be defined outside classes
    # take that 1st year university test questions
    cls.__repr__ = __repr__

    # returns itself because of decorator(class) syntax
    return cls



class Singleton:
    """
    Singleton class based off of:
        https://colab.research.google.com/drive/1eajT5Rl9tA-7RmSHMME54B81U5aSKSni#scrollTo=nfQZINGxuUdK

    Sets its own attributes based off of:
        https://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python
    """

    def __new__(cls, *args, **kwargs):
        attr_name = f"_{cls.__name__}"
        if not hasattr(cls, attr_name):
            try:
                # generally for namedtuple, which works even if no args/kwargs are given
                attribute = super().__new__(cls, *args, **kwargs)
            except TypeError as e:
                if e.args[0] == "object() takes no parameters":
                    # for a regular object that has an __init__
                    attribute = super().__new__(cls)
                else:
                    exc_add_msg(e, f'with class {cls.__qualname__}')
                    raise

            setattr(cls, attr_name, attribute)
        return getattr(cls, attr_name)

"""
Simply provides the encode/decode function to turn a literal string into a regular string and back
"""

def decode_str(string):
    r"""
    Removes the quotations around a string, replaces double \\ with \, and replaces
    any specific character representation starting with \ with its true character
    (eg. \n turns to a newline)
    """
    if not len(string) >= 2:
        raise SyntaxError(f"Expected the string {string!r} to be longer than two characters so it can begin and end with a quotation")
    if not string.startswith('"'):
        raise SyntaxError(f"Expected the string {string!r} to begin with a quotation")
    if not string.endswith('"'):
        raise SyntaxError(f"Expected the string {string!r} to end with a quotation")

    return codecs.decode(string[1:-1], "unicode_escape")

def encode_str(string):
    r"""
    Surrounds the string with (double) quotes and replaces any characters with backslashes
    to their character representations
    """
    return '"' + codecs.encode(string, "unicode_escape").decode("utf-8") + '"'


if __name__ == "__main__":
    pass

