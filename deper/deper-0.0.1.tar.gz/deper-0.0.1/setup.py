#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(name="deper",  # 项目名
      version="0.0.1",       # 版本号
      description="项目部署工具",  #简介
      long_description=long_description,  # 长简介 这里使用的 readme 内容
      long_description_content_type="text/markdown",
      license="BSD",   # 授权
      install_requires=requirements, # 依赖
      author="toalaska",  # 作者
      author_email="toalaska@126.com",  # 邮箱
      url="https://github.com/toalaska/deploy",  # 地址
      download_url="https://github.com/toalaska/deploy/archive/master.zip",
      packages=find_packages("deploy"),
      keywords=["deploy", "oss","ssh"],
      zip_safe=True)