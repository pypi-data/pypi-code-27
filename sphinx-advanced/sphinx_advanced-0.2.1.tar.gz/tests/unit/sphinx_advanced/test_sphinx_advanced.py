# -*- coding: utf-8 -*-


"""Unit Tests for `sphinx_advanced` package."""


from sphinx_advanced import sphinx_advanced


def test_help():
    """sphinx_advanced :: Unit :: sphinx_advanced :: help"""
    assert sphinx_advanced.help() == 'Sphinx Advanced Tutorial Module'
