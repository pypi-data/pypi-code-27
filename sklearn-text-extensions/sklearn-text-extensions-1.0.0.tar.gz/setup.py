#!/usr/bin/env python
from setuptools import find_packages, setup

project = "sklearn-text-extensions"
version = "1.0.0"

setup(
    name=project,
    version=version,
    description="Scikit-learn compatible text feature extraction extensions",
    author="Globality Engineering",
    author_email="engineering@globality.com",
    url="https://github.com/globality-corp/sklearn-hierarchical-classification",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "numpy>=1.14.3",
        "scikit-learn>=0.19.1",
        "scipy>=1.1.0",
    ],
    setup_requires=[
        "nose>=1.3.7",
    ],
    tests_require=[
        "coverage>=3.7.1",
        "PyHamcrest>=1.9.0",
    ],
)
