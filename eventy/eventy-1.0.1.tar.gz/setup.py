#!/usr/bin/env python

from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

if __name__ == '__main__':
    setup(
        name='eventy',
        version='1.0.1',
        url='https://github.com/qotto/eventy',
        license='MIT',
        author='Alexandre Syenchuk',
        author_email='sacha@qotto.net',
        description='Qotto/eventy',
        long_description=readme,
        long_description_content_type='text/markdown',
        packages=find_packages(exclude=['tests']),
        python_requires='>=3.6',
        include_package_data=True,
        zip_safe=False,
        install_requires=[],
        classifiers=[
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3.6',
        ],
    )
