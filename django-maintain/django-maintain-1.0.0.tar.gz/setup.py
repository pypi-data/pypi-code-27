# -*- coding: utf-8 -*-

from setuptools import setup

version = '1.0.0'


setup(
    name='django-maintain',
    version=version,
    keywords='Django Maintain Notice',
    description='Django Maintain Notice',
    long_description=open('README.rst').read(),

    url='https://github.com/Brightcells/django-maintain',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['maintain'],
    py_modules=[],
    install_requires=['django-six'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
)
