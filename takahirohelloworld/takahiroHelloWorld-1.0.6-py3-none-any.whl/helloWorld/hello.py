#!/usr/bin/env python3
#!-*- coding: utf8 -*-
import sys


def say_hello(name=None):
    if name is None:
        print("hello, world!")
    else:
        print("hello, {}!".format(name))


def main():
    if len(sys.argv) == 2:
        name = sys.argv[1]
    else:
        name = None
    say_hello(name)
