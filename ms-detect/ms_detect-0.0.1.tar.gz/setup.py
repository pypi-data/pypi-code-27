from distutils.core import setup
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="ms_detect",
    version="0.0.1",
    description="micor soft detect",
    long_description=long_description,
    long_description_content_type="text/markdown",

    license = "MIT",
    author="zhaomingming",
    author_email="13271929138@163.com",
    url="http://www.zhaomingming.cn",
    py_modules=['ms_detect'],
    platforms = 'any'
)
