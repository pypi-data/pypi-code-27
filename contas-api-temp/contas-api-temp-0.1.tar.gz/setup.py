import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="contas-api-temp",
    version="0.1",
    author="Felippe",
    author_email="felippemsc@gmail.com",
    description="API para gestão de finanças",
    long_description=README,
    url="https://github.com/felippemsc/testeOrama",
    include_package_data=True,
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: BSD License",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        'Topic :: Internet :: WWW/HTTP',
    ),
)
