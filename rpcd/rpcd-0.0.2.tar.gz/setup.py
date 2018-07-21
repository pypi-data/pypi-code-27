from setuptools import setup, find_packages
import os


setup(
    name='rpcd',
    version='0.0.2',
    description='Remote procedure call daemon server for mysql',
    long_description='A remote procedure call mysql database server with PyQt5 interface',
    author='Dr Abiira Nathan',
    author_email='nabiira2by2@gmail.com',
    license='GPL-3',
    platforms=['Windows 7','Windows 8', 'Windows 10', 'Linux/Unix'],
    keywords ='mysql server daemon Abiira Nathan rpcd',
    packages = find_packages(),
    install_requires=['mysql-connector-python', 'PyQt5'],
    )
