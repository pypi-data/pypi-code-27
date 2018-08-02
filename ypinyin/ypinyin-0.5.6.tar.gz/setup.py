# -*- coding: utf-8 -*-
import os
import io
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = io.open(os.path.join(here, 'README.rst'), encoding='UTF-8').read()
CHANGES = io.open(os.path.join(here, 'CHANGES.rst'), encoding='UTF-8').read()

setup(name="ypinyin",
      version='0.5.6',
      description="translate chinese hanzi to pinyin by python",
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='pinyin',
      author="Eric Lo",
      author_email="liuguangyuan0532@gmail.com",
      url="https://github.com/liuguangyuan0532/ypinyin",
      packages=find_packages('src'),
      install_requires=[
         'xpinyin>=0.5.5', 
      ],
      test_suite='ypinyin.tests',
      package_dir={'': 'src'},
      include_package_data=True,
      license="BSD")
