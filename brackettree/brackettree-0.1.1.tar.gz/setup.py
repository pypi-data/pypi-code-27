#!/usr/bin/python3
# -*- coding: utf-8 -*-
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

from setuptools import setup


setup(
    name="brackettree",
    version='0.1.1',

    description="Create tree structure out of a string with brackets.",

    author="Vojtěch Pachol",
    author_email="pacholick@gmail.com",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
    ],
    keywords="python, parsing",

    # packages=find_packages(exclude=["contrib", "docs", "tests*", "latex"]),
    packages=["brackettree"],

    # install_requires=[],
)
