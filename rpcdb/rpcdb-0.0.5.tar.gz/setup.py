from setuptools import setup, find_packages
import os


setup(
    name='rpcdb',
    version='0.0.5',
    description='A multiplatform mysql framework for client-server apps',
    long_description="rpcdb is an abstraction around mysql-connector-python"
    " that enable connection to remote mysql database using multiprocessing"
    " remote connection. Features a mysql to tkinter relational mapper "
    " e.g VARCHAR represents a ttk.Entry field, Text represents tkinter.scrolledtext.ScrolledText"
    " One stop package for general purpose classes, decorators and functions. "
    " Has a commandline chat server that can be accessed by multiple GUI clients",
    url='https://github.com/abiiranathan/rpcdb.git',
    author='Dr Abiira Nathan',
    author_email='nabiira2by2@gmail.com',
    license='GPL-3',
    platforms=['Windows 7','Windows 8', 'Windows 10', 'Linux/Unix'],
    keywords ='mysql database python Abiira Nathan framework rpcdb tkinter relational mapper',
    packages = find_packages(),
    install_requires=['mysql-connector-python'],
    )
