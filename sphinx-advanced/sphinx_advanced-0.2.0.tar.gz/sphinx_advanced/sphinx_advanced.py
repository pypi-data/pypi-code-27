# -*- coding: utf-8 -*-

"""Main module

.. note:: Proof of Concept

.. module:: sphinx_advanced.sphinx_advanced
    :platform: OS X
    :synopsis: sphinx advanced tutorial project

.. moduleauthor:: Julio Antúnez Tarín <julio.antunez.tarin@gmail.com>

Usage:
    from sphinx_advanced import sphinx_advanced
"""


def help():
    """Sphinx Advanced Module help

    .. todo:: Add more sample modules and some subpackage

    Args:
        none

    Retuns:
        A brief description of the module

    """
    return 'Sphinx Advanced Tutorial Module'


def init():
    """Print ``help()`` when run as a script.

    Args:
        none

    Retuns:
        :func:`sphinx_advanced.sphinx_advanced.help()`
    """
    if __name__ == "__main__":
        print(help())


init()
