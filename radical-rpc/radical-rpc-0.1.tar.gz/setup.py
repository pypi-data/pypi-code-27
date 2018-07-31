#!/usr/bin/env python3.6

# coding=utf-8

from setuptools import setup

setup(
    name='radical-rpc',
    version='0.1',
    description='Multi-transport RPC with asyncio & Django support.',
    author="Andrew Dunai",
    author_email='andrew@dun.ai',
    url='https://github.com/and3rson/radical',
    license='GPLv3',
    packages=[
        'radical',
        'radical.transports',
        'radical.management',
        'radical.management.commands',
        'radical.serialization',
        'radical.contrib',
        'radical.contrib.django',
    ],
    include_package_data=True,
    install_requires=['aioredis'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: AsyncIO',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='rpc,python2,python3,python,asyncio,aio,redis,django',
)
