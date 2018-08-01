#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "is99kdf",
    version = "0.1.0",
    keywords = ("pip", "is99kdf"),
    description = "python tools by dengfeng.ke",
    long_description = "python tools by dengfeng.ke",
    license = "BJFU Licence",

    url = "https://github.com/",
    author = "is99kdf",
    author_email = "dengfeng.ke@beijinghear.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["scipy","numpy","librosa"]
)

