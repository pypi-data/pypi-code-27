#!/usr/bin/python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
try:
    from foebackend import __version__
except ImportError:
    try:
        import re
        with open('backend/foebackend/__init__.py') as f:
            __version__ = re.search(
                r'^__version__\s*=\s*[\'"]([^"\']+)', f.read(), re.MULTILINE
            ).group(1)
    except Exception:
        __version__ = '1.0.0'

setup(
    name="foebackend",
    version=__version__,

    description="FareOn eshop backend",

    author="Vojtěch Pachol",
    author_email="v.pachol@mikroelektronika.cz",

    # license="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
    ],
    keywords="python, eshop, fareon",

    packages=find_packages(exclude=["contrib", "docs", "tests*", "latex"]),
    # packages=["fareoneshop"],

    install_requires=["tornado<5", "motor<2", "schematics", "python-dateutil",
                      "PyJWT", "PyYAML", "pycrypto", "Babel"],

    package_data={
        'foebackend': ['translations/*', 'templates/*/*/*'],
    },

    entry_points={
        "console_scripts": [
            "foebackend=foebackend:main",
        ],
    },
)
