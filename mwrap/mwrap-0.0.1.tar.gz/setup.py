#!/usr/bin/env python

# Copyright 2018 Daniel Zalevskiy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name="mwrap",
    version="0.0.1",
    author="Daniel Zalevskiy",
    author_email="dndanik@gmail.com",
    description="Utilities for managing meson subprojects",
    url="https://github.com/CPB9/mwrap.git",
    packages=setuptools.find_packages(),
    install_requires=["colorama"],
    classifiers=(
        "Environment :: Console",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7', #trusty, xenial, bionic
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4', #trusty
        'Programming Language :: Python :: 3.5', #xenial
        'Programming Language :: Python :: 3.6', #bionic
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'mwrap = mwrap.main:main',
        ],
    }

)
