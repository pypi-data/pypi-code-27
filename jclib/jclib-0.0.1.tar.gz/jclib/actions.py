"""
Use this module to write performable, confirmable actions
"""

import abc
from distutils.util import strtobool


class Action(metaclass=abc.ABCMeta):

    """
    A performable, confirmable action.

    Example usage:
    >>> class Echo(Action):
    ...     description = "Echo text: '{text}'"
    ...     def __init__(self, text):
    ...         self.text = text
    ...     def perform(self):
    ...         print(self.text)
    ...
    >>> hello = Echo("hello")
    >>> str(hello)
    "Echo text: 'hello'"
    >>> hello.perform()
    hello
    """

    description: str

    @abc.abstractmethod
    def perform(self):
        pass

    def __str__(self):
        return self.description.format(**self.__dict__)


def confirm(prompt, default=False):
    """Give a yes/no prompt with the default letter (y or n) presented as uppercase"""
    if default:
        prompt += " [Y/n] "
    else:
        prompt += " [y/N] "
    response = None

    while response is None:
        raw_input = input(prompt)
        if raw_input == "":
            response = default
            break
        try:
            response = strtobool(raw_input)
        except ValueError:
            continue
    return bool(response)
