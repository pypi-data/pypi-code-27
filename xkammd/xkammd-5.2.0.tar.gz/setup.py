# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 11:37
# @Author  : LI Jiawei
# @Email   : jliea@connect.ust.hk
# @File    : setup.py
# @Software: PyCharm

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xkammd",
    version="5.2.0",
    author="LI Jiawei",
    author_email="jliea@connect.ust.hk",
    description="You know how I love you",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ricarvy/bbwdxka",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)