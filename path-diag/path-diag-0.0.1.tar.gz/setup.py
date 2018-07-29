from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="path-diag",
    version="0.0.1",
    license="MIT",
    entry_points={"console_scripts": ["pathdiag=src.pathdiag:main"]},
    description=(
        "A utility for validating paths in environment variables and "
        "modifying them safely"
    ),
    scripts=['bash/path-diag-functions.sh'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rigas Papathanasopoulos",
    author_email="rigaspapas@gmail.com",
    url="https://www.rigaspapas.com",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=["colorama"],
    data_files=[('scripts', ['bash/path-diag-functions.sh'])],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
