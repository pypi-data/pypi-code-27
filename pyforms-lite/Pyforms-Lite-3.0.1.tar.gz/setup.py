#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

setup(
	name='Pyforms-Lite',
	version='3.0.1',
	description='Pyforms-Lite is a Python 2.7 and 3.5 framework to develop GUI applications based on PyQt',
	author='Nikhil Narayana',
	author_email='nikhil.narayana@live.com',
	license='MIT',
	url='https://github.com/NikhilNarayana/pyforms-lite',
	install_requires=[
		'AnyQt',
		'PyQt5',
		'python-dateutil',
		'numpy',
	],
	packages=find_packages(),
	package_data={'pyforms': [
		'gui/controls/uipics/*.png',
		'gui/mainWindow.ui', 'gui/controls/*.ui']
	},
)
