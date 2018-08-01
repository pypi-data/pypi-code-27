#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: dengfeng.ke
# Mail: dengfeng.ke@beijinghear.com
# Created Time:  2018-8-1 16:13
#############################################


from setuptools import setup, find_packages

setup(
    name = "is99kdf",
    version = "0.4.1",
    keywords = ("pip", "is99kdf"),
    description = "python tools by dengfeng.ke",
    long_description = "python tools by dengfeng.ke",
    license = "BJFU Licence",

    url = "https://pypi.org/project/is99kdf/",
    author = "is99kdf",
    author_email = "dengfeng.ke@beijinghear.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["scipy","numpy","librosa"]
)

