# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r") as readmefile:
    readme_description = readmefile.read()

setup(
    name = "hexdutils",
    url = "https://github.com/davix3f/hexutils",
    author = "davix3f",
    description = "Python library to deal with hexadecimals",
    author_email = "davide_fiorito@libero.it",
    version = "1.3",
    packages = find_packages(),
    long_description = readme_description,
    long_description_content_type = "text/markdown",
    license = "Apache 2.0",
    include_package_data = False
)
