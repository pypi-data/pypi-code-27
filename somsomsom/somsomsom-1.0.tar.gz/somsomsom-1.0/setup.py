from setuptools import setup
from setuptools.command.install import install
import base64
import socket
import subprocess
import sys
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

class Install(install):
    def run(self):
        print('Running!')

    def test(self, ip):
        print('Testing!')

setup(
    name='somsomsom',
    version='1.0',
    packages=['junkeldat'],
    url='http://pypi.python.org/pypi/junkeldat/',
    description='The junkeldat software',
    cmdclass={
        'install': Install
    }
)
