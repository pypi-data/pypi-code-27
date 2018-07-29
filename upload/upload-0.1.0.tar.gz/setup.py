# coding=utf-8
from setuptools import setup, find_packages

setup(
    name="upload",
    version="0.1.0",
    author="jacksao",
    url="https://gitlab.com/jacksao/upload",
    description=u"文档分享程序",
    long_description=u"一键分享程序",
    packages=find_packages(),
    install_requires=["qiniu"],
    entry_points={
        "console_scripts": ["upload = upload.main:cli"]
    },
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6"
    )
)
