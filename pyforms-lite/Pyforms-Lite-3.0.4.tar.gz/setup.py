#!/usr/bin/python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

long_des = ""
with open(path.join(here, 'README.md')) as f:
    long_des = f.read()

setup(
	name='Pyforms-Lite',
	version='3.0.4',
	description='Pyforms-Lite is a Python 2.7 and 3.5 framework to develop GUI applications based on PyQt',
	long_description=long_des,
	long_description_content_type="text/markdown",
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
	package_data={'pyforms_lite': [
		'gui/controls/uipics/*.png',
		'gui/mainWindow.ui', 'gui/controls/*.ui']
	},
)
