from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sydsvenskan',
    version='0.3.0',
    description='Module for searching sydsvenskan.se',
    long_description=readme,
    author='Peter Stark',
    author_email='peterstark72@gmail.com',
    url='https://github.com/peterstark72/py-sydsvenskan',
    license=license,
    install_requires=['requests>=2.19.1', 'lxml>=4.2.3','pyRFC3339>=1.1'],
    packages=find_packages(exclude=('tests', 'docs'))
)
