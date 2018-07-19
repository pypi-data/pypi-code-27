from setuptools import setup

setup(name='accoladecli', version='2.1', packages = ['cliparser'], author= 'J.V.', description= 'Accolade CLI'
      ,scripts=['cliparser/accolade'], install_requires= ['boto3'])
