import io
import re
from os.path import join, abspath, dirname
from setuptools import setup


def read(name):
    here = abspath(dirname(__file__))
    return io.open(
        join(here, name), encoding='utf8'
    ).read()


setup(
    name="pypi-code-highlighting-demo",
    version="0.1.13",
    author='Patryk Galczynski',
    author_email='galczynski.patryk@gmail.com',
    url='https://github.com/evemorgen/pypi-code-highlighting-demo',
    description='This is a example package that will show how syntax highlighting on PyPI project page works',
    long_description='%s\n%s' % (
        read('README.rst'),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    keywords=[
        'syntax', 'highlighting', 'example', 'rst', 'render'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX',
        'Development Status :: 4 - Beta'
    ]
)
