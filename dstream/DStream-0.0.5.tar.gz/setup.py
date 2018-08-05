# -*- coding: utf8 -*-
from distutils.core import setup

try:
    long_description = open('README.rst').read()
except Exception:
    long_description = ''

setup(
    name='DStream',
    version='0.0.5',
    description='An experimental Java-8-stream-like lib.',
    long_description=long_description,
    author='manxisuo',
    author_email='manxisuo@gmail.com',
    platforms=["all"],
    url='https://github.com/manxisuo/dstream',
    package_dir={'dstream': 'src'},
    packages=['dstream'])
