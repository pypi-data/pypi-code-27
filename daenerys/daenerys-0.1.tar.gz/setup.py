# coding=utf-8
from os.path import join, dirname
from setuptools import setup, find_packages

VERSION = (0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

with open(join(dirname(__file__), 'README.md')) as f:
    long_description = f.read().strip()

setup(
    name = 'daenerys',
    description = 'Scraping and Web Crawling Framework',
    url = 'https://code.pycourses.com/courses/daenerys',
    long_description = long_description,
    version = __versionstr__,
    author = 'Dong Weiming',
    author_email = '61966225@qq.com',
    packages=find_packages(),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
