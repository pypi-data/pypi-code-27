# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import versioneer

setup(
    name='aerosol_optprop',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Optical property calculations of aerosol aerosol_optprop',
    author='Landon Rieger',
    author_email='landon.rieger@canada.ca',
    url='https://gitlab.com/LandonRieger/aerosol_optprop',
    license='MIT',
    packages=find_packages(),
    package_data={'aerosol_optprop': ['data/refractive_index']},
    include_package_data=True,
    install_requires=['numpy', 'miepython']
)