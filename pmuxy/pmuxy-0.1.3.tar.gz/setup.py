from setuptools import setup, find_packages

required = [
    'click',
    'libtmux',
    'pyyaml'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    description='A tmux windows manager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
    name='pmuxy',
    packages=find_packages(exclude=['tests']),
    url="https://github.com/SAReyes/pmuxy",
    scripts=['bin/pmuxy'],
    version='0.1.3'
)

