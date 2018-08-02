#!/usr/bin/env python3
import codecs
import os
import subprocess

import sys
from setuptools import setup

from Resources.Requirements import pip_requires

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

# print(os.getcwd())
# subprocess.run(["./Commands/link-commands", "-f"])

setup(
    name='lztools',
    author='Laz aka Zanzes',
    author_email='ubuntuea@gmail.com',
    version='1.1.14',
    license='MIT License',
    description='A collection of useful utilities by Laz aka Zanzes',
    url='',
    entry_points={
        'console_scripts': [
            'lztools = cli.lztools:main',
            'preg = cli.preg:main',
            'lmod = cli.lmod:main',
            'ldoc = cli.ldock:main',
            'lgit = cli.lgit:main'
        ],
    },
    install_requires=pip_requires,
    packages=['lztools', 'cli', 'lztools.Managers', 'lztools.DataTypes', 'lztools.Data', 'lztools.Junk', 'Resources'],
    zip_safe=False,
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: System :: Systems Administration',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
    ],
)

