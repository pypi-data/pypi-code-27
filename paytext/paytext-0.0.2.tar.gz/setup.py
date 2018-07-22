# pyre-strict

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='paytext',
    version='0.0.2',
    author='Yngve Høiseth',
    author_email='yngve@hoiseth.net',
    description='Generalize texts from payment card transactions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yhoiseth/paytext',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
