import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-cpffield',
    version='0.1',

    description='CPF Field to use in Django Model Form',
    url='https://github.com/silviolleite/cfp-field',

    # Author details
    author='Silvio Luis Leite',
    author_email='silviolleite@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # example license
    long_description=README,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
