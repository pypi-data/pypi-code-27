#!/usr/bin/env python

try:
    from setuptools import setup

    setup(name='phonetic2bengali',
          version='1.0.1',
          description='convert bengali text written in english to bengali while keeping english ony text',
          long_description=open('README.rst', 'rt').read(),
          author='Subrata Sarkar',
          author_email='subrotosarkar32@gmail.com',
          url='https://github.org/SubrataSarkar32/phonetic2bengali/',
          packages=['phonetic2bengali','phonetic2bengali.pyavrophonetic','phonetic2bengali.pyavrophonetic.utils'],
          package_data = {'': ['*.txt', '*.json','*.rst']},
          include_package_data = True,
          install_requires=["simplejson >= 3.0.0","pyenchant >= 2.0.0"],
          license='Apache v2.0',
          classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            ]
          )

except ImportError:
    print('Install setuptools')
