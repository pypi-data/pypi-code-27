#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
        name='eventy',
        version='1.0.0',
        url='https://github.com/qotto/eventy',
        license='MIT',
        author='Alexandre Syenchuk',
        author_email='sacha@qotto.net',
        description='Qotto/eventy',
        packages=['eventy'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[

        ],
        classifiers=[
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3.6',
        ],
    )
