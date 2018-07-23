# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

import adpushup_adstxt

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="adpushup-adstxt",
    version=adpushup_adstxt.VERSION,
    description="AdPushUp ads.txt management API.",
    author="Roman Barczyński",
    author_email="romanb@leanlab.pl",
    url="https://bitbucket.org/romkenet/adpushup-adstxt/",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    include_package_data=True,
    setup_requires=["setuptools_git"],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
