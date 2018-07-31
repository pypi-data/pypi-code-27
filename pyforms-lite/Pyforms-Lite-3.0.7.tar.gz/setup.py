#!/usr/bin/python
from setuptools import setup, find_packages
from os import path

setup(
	name='Pyforms-Lite',
	version='3.0.7',
	description='Pyforms-Lite is a Python 2.7 and 3.5+ framework to develop GUI applications based on PyQt',
	long_description_content_type="text/markdown",
	author='Nikhil Narayana',
	author_email='nikhil.narayana@live.com',
	license='MIT',
	url='https://github.com/NikhilNarayana/pyforms-lite',
	install_requires=[
		'AnyQt',
		'PyQt5',
	],
	packages=find_packages(),
	package_data={'pyforms_lite': [
		'gui/controls/uipics/*.png',
		'gui/mainWindow.ui', 'gui/controls/*.ui']
	},
)
