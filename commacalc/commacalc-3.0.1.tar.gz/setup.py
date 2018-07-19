#!/usr/bin/python3
# Copyright (C) 2016  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import fastentrypoints      # noqa: F401


setup(
    name="commacalc",
    version='3.0.1',

    description="Command line calc",
    # long_description=long_description,

    author="Vojtěch Pachol",
    author_email="pacholick@gmail.com",

    license="LGPL-3.0",

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
    ],
    keywords="python, math, calc",

    packages=find_packages(exclude=["contrib", "docs", "tests*"]),

    install_requires=["fastentrypoints", "colorama", "httplib2"],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     "": ["*.ui"],
    # },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        "console_scripts": [
            ",=commacalc:main",
        ],
    },
)
