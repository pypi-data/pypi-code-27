# -*- coding: utf-8 -*-

"""Main module."""

def message():
	"""Some function for testing pypi package building"""
	name = str(raw_input("Enter your name: "))
	print("Hello {usr_name}! Welcome to Shanghai!".format(usr_name=name))