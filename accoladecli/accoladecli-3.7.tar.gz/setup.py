from setuptools import setup
import importlib.machinery as mh
from cliparser import _version


# helper = mh.SourceFileLoader('__init__', '/Users/vikram.chandran/Desktop/Repos/accoladecli/cliparser/__init__.py')
# accolade = helper.load_module()

if __name__ == '__main__':
    version_num = _version.__version__
print('This is the version number: {}'.format(version_num))


setup(name='accoladecli', version = version_num, packages = ['cliparser'], author= 'J.V.', description= 'Accolade CLI',
      scripts=['cliparser/accolade'], install_requires= ['boto3', 'botocore', 'pipdate'])
