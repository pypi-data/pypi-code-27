# -*- coding: utf-8 -*-

"""Main module

.. note:: Proof of Concept

.. module:: python_testing_advanced.python_testing_advanced
    :platform: OS X
    :synopsis: sphinx advanced tutorial project

.. moduleauthor:: Julio Antúnez Tarín <julio.antunez.tarin@gmail.com>

Usage:
    from python_testing_advanced import python_testing_advanced
"""


def help():
    """Python Testing Advanced Module help

    .. todo:: Add some subpackage

    Args:
        none

    Retuns:
        A brief description of the module

    """
    return 'Python Testing Advanced Tutorial Module'


def init():
    """Print ``help()`` when run as a script.

    Args:
        none

    Retuns:
        :func:`python_testing_advanced.python_testing_advanced.help()`
    """
    if __name__ == "__main__":
        print(help())


init()
