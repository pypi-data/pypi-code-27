# -*- coding: utf-8 -*-


"""Unit Tests for `python_testing_advanced` package."""


from python_testing_advanced import python_testing_advanced


def test_help():
    """Unit :: python_testing_advanced :: help"""
    assert python_testing_advanced.help() == \
        'Python Testing Advanced Tutorial Module'
