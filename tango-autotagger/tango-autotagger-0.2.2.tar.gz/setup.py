# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

#with open('docs/requirements.txt') as f:
#    required = f.read().splitlines()

setup(
    name='tango-autotagger',
    version='0.2.2',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    url='http://github.com/tBaxter/autotagger',
    license='LICENSE',
    description="""
        Takes a given block of text and tags it according to Django models
        and fields defined in settings""",
    long_description=open('README.md').read(),
    packages=find_packages(),
    #install_requires=required,
    zip_safe=False,
    include_package_data=True,
)
