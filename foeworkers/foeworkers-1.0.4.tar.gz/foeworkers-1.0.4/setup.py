#!/usr/bin/python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name="foeworkers",
    version='1.0.4',

    description="FareOn eshop workers",

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

    install_requires=["tornado<5", "motor<2", "zeep", "PyYAML"],
    # "foebackend"],  # musel bych to nějak zařadit do indexu

    package_data={
        'foeworkers': ['templates/*/*', 'transactionchecker/bbdirect-wsdl/*'],
    },

    entry_points={
        "console_scripts": [
            "foemailer=foeworkers.mailer:main",
        ],
    },
)
