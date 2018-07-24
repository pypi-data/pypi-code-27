# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Email:  hhczy1003@163.com
# @Date:   2017-08-01 20:37:27
# @Last Modified by:   hang.zhang
# @Last Modified time: 2018-07-24 16:59:25

from setuptools import setup

setup(
    name="DBService",
    version="1.1",
    author="yiTian.zhang",
    author_email="hhczy1003@163.com",
    packages=["DBService"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "scrapy",
        "scrapy-redis",
        "pymongo",
        "apscheduler",
        "selenium",
    ],
)
