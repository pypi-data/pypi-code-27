# -*- coding: utf-8 -*-


"""Unit Tests for `sphinx_advanced.calculator` module."""


from sphinx_advanced import calculator


def test_addition():
    """sphinx_advanced :: Unit :: calculator :: addition"""
    assert calculator.addition(1, 2) == 3


def test_substraction():
    """sphinx_advanced :: Unit :: calculator :: substraction"""
    assert calculator.substraction(3, 2) == 1


def test_multiplication():
    """sphinx_advanced :: Unit :: calculator :: multiplication"""
    assert calculator.multiplication(2, 3) == 6


def test_division():
    """sphinx_advanced :: Unit :: calculator :: division"""
    assert calculator.division(10, 5) == 2


def test_exponential():
    """sphinx_advanced :: Unit :: calculator :: exponential"""
    assert calculator.exponential(2, 3) == 8
