#!/usr/bin/python3
# encoding: utf-8


from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="jeffrain",  # 这里是pip项目发布的名称
    version="1.1",  # 版本号，数值大的会优先被pip
    description="just a tool set",

    author="J",
    author_email="z.798818344@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    #     install_requires=["numpy"]  # 这个项目需要的第三方库
)
