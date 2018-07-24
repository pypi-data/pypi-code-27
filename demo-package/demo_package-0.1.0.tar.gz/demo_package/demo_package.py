# -*- coding: utf-8 -*-

"""Main module."""


def add(a, b, c):
    if not (type(a) == type(b) == type(c)):
        raise TypeError("arguments a, b, c must have same type")
    return a + b + c

def sumup_file(path):
    numbers = []
    for line in open(path, "r"):
        numbers.append(float(line))
    return sum(numbers)


def mult(a, b, c):
    return a * b * c

