#!/usr/bin/python
# coding: utf-8
# (c) 2017 Raul Granados <@pollitux>

from setuptools import setup, find_packages

version = "1.0.5"
author = "Tingsystems"

setup(
    name='toshare',
    version=version,
    author=author,
    author_email='soporte@tingsystems.com',
    url='https://github.com/tingsystems/toshare-python',
    description='Easy ToShare python wrapper',
    long_description=open('./README.txt', 'r').read(),
    download_url='https://github.com/tingsystems/toshare-python/master',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(),
    install_requires=[
        'requests',
        'simplejson',
        'nose'
    ],
    license='MIT License',
    keywords='toshare wrapper',
    include_package_data=True,
    zip_safe=True,
)
