"""
this is the test module doc string
"""

import src.main as main


def test_hello():
    """
    test hello ds
    Returns:
        None

    """
    assert main.hello() == 0


def test_stupid():
    """
    this is a really stupid test
    Returns:

    """
    assert 1 == 1
