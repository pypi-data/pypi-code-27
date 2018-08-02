from setuptools import setup, find_packages

required = [
    'click',
    'libtmux',
    'pyyaml'
]

setup(
    description='A tmux windows manager',
    install_requires=required,
    name='pmuxy',
    packages=find_packages(exclude=['tests']),
    scripts=['bin/pmuxy'],
    version='0.1.1'
)

