import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='abel',
    version='0.0.4',
    author='Hunan Rostomyan',
    author_email='hunan131@gmail.com',
    description='Machine learning components',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hunan-rostomyan/abel',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
