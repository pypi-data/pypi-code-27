#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the fingerd Python 3.x module, which is MIT-licensed.
#******************************************************************************
""" Setup script for the textoutpc Python package and script. """

from setuptools import setup, find_packages

setup(name='textoutpc',
	version='0.1',
	description='Textout() equivalent from Planète Casio',
	author='Thomas "Cakeisalie5" Touhey',
	author_email='thomas@touhey.fr',
	url='https://forge.touhey.fr/pc/textout.git/',
	license='MIT',
	keywords='planète casio textout bbcode translator parser',

	packages=find_packages(),
	scripts=['textout2html', 'textout2lightscript'],
	test_suite="test",

	install_requires=['regex'],

	classifiers = [
		'Development Status :: 2 - Pre-Alpha',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: French',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Intended Audience :: Developers',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
		'Topic :: Text Processing :: Markup :: HTML'
	]
)

# End of file.
