# -*- coding: utf-8 -*-

"""Main module."""


def message(name):
    """Some function for testing pypi package building"""
    if name == "":
        name = "pretend person"
    print("Hello {usr_name}! Welcome to Shanghai!".format(usr_name=name))
