from setuptools import setup

import os
import re
import stat

def version():
    with open(os.path.abspath(__file__).replace('setup.py', 'version.meta'), 'r') as v:
        return v.read()

def _readfile(file_name):
    with open(os.path.abspath(__file__).replace('setup.py', file_name), 'r') as v:
        lines = v.readlines()
    return list(filter(lambda x: re.match('^\w+', x), lines))


def requirements():
    return _readfile('requirements.txt')

setup(
    name='aiot-studio',
    version=version(),
    author='mnubo, inc.',
    author_email='support@mnubo.com',
    url='https://smartobjects.mnubo.com/documentation/sdks.html',
    packages=['aiotstudio', 'aiotstudio._core'],
    install_requires=requirements(),
    include_package_data=True
)
