
#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xingming
# Mail: user@gmail.com
# Created Time:  2018-07-31 15:00:01 PM
#############################################


from setuptools import setup, find_packages

setup(
    name = "soinlocal",
    version = "0.1.1",
    keywords = ("pip", "server","so"),
    description = "so.com",
    packages = ["soinlocal"],
    long_description = "so in local: 127.0.0.1",
    license = "MIT Licence",

    url = "https://github.com/ghubgituse/so.git",
    author = "git",
    author_email = "usegithub@126.com",

    #packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['requests', 'flask']
)
