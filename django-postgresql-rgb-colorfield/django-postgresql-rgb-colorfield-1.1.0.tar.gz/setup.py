import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-postgresql-rgb-colorfield',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='Mozilla Public License 2.0 (MPL 2.0)',  # example license
    description='A ColorField to save Colors in RGB array in postgresql.',
    long_description=README,
    url='https://gitlab.com/codesigntheory/django-postgresql-rgb-colorfield',
    author='Utsob Roy',
    author_email='roy@codesign.com.bd',
    install_requires = [
        'webcolors'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
