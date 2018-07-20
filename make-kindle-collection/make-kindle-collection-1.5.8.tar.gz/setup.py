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

from setuptools import setup
import fastentrypoints      # noqa: F401


setup(
    name="make-kindle-collection",
    version='1.5.8',

    description="Make Kindle collection",

    author="Vojtěch Pachol",
    author_email="pacholick@gmail.com",

    license="LGPL-3.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
    ],
    keywords="python, ebook, kindle",

    packages=["mkc"],
    install_requires=["fastentrypoints", "brackettree",
                      "httplib2", "beautifulsoup4", "cairosvg", "Pillow"],
    data_files=[("/usr/share/mkc/latex", ["latex/main.tex"])],
    entry_points={
        "console_scripts": [
            "mkc=mkc:main",
        ],
    },
)
