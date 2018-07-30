from setuptools import setup

setup(
    name='mokt',
    version='0.9',
    packages=['mokt'],

    description='A simple framework for automated testing of OpenCL kernels',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    license='CC0 1.0',
    author='Band of Four',
    url='https://github.com/band-of-four/master-of-kernel-testing',

    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ],

    install_requires=[
        'tensorflow>=1.5',
        'pyopencl',
        'termcolor'
    ]
)
