import os
from setuptools import setup

def read(filename):
    return open(os.path.join(os.getcwd(), filename)).read()

setup(
    name='dotrc',
    description='Simple .rc file loading for your Python projects',
    author='Paul Holden',
    author_email='pholden@stria.com',
    version='0.1',
    packages=['dotrc'],
    package_dir={'': 'src'},
    url='https://pypi.org/project/dotrc/',
    project_urls={
        'GitHub': 'https://github.com/paulholden2/dotrc'
    },
    license='MIT',
    install_requires=['PyYAML','simplejson'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords='dot rc config file',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ]
)
