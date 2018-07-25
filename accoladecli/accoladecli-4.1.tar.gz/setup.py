from setuptools import setup
from cliparser._version import __version__ as version_num

print('This is the version number: {}'.format(version_num))


setup(name='accoladecli', version = version_num, packages = ['cliparser'], author= 'J.V.', description= 'Accolade CLI',
      scripts=['cliparser/accolade'], install_requires= ['boto3', 'botocore', 'pipdate'])
