from setuptools import setup
from cliparser import __init__

version_num = 2.5

setup(name='accoladecli', version= version_num, packages = ['cliparser'], author= 'J.V.', description= 'Accolade CLI'
      ,scripts=['cliparser/accolade'], install_requires= ['boto3', 'botocore', 'pipdate'])
