from setuptools import setup, find_packages
import os


setup(
    name='rpcdb',
    version='0.0.3',
    description='A multiplatform mysql framework for client-server apps',
    long_description="rpcdb is an abstraction around mysql-connector-python"
    " that enable connection to remote mysql database using multiprocessing"
    " remote connection",
    url='https://github.com/abiiranathan/rpcdb',
    author='Dr Abiira Nathan',
    author_email='nabiira2by2@gmail.com',
    license='GPL-3',
    platforms=['Windows 7','Windows 8', 'Windows 10', 'Linux/Unix'],
    keywords ='mysql db2 database python3.6 Abiira Nathan',
    packages = find_packages(),
    install_requires=['mysql-connector-python'],
    )
