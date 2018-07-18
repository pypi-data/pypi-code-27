# -*- coding: utf-8 -*-

#   Copyright 2018 Jim Martens
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""setup.py: build script for setuptools"""
from setuptools import setup, find_packages

with open("README.md", "rb") as f:
    long_desc = f.read().decode()

setup(
    name="twomartens.calendarsync",
    description="Tool that synchronizes Jekyll event collection with remote calendar",
    long_description=long_desc,
    long_description_content_type="text/markdown; charset=UTF-8",
    author="Jim Martens",
    author_email="github@2martens.de",
    url="https://git.2martens.de/2martens/calendar-synchronization",
    version="1.0.1",
    namespace_packages=["twomartens"],
    packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'': 'src'},
    package_data={
        'twomartens.calendarsync': ['event_template.markdown'],
    },
    entry_points={
        "console_scripts": ['tm-calendarsync = twomartens.calendarsync.calendarsync:main']
    },
    python_requires="~=3.6",
    install_requires=["ics>=0.4"],
    license="Apache License 2.0",
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
