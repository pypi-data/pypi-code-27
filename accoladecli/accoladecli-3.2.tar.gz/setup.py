from setuptools import setup
import importlib.machinery as mh


helper = mh.SourceFileLoader('accolade', '/Users/vikram.chandran/Desktop/Repos/accoladecli/cliparser/accolade')
accolade = helper.load_module()

version_num = accolade.version
print(version_num)


setup(name='accoladecli', version = version_num, packages = ['cliparser'], author= 'J.V.', description= 'Accolade CLI',
      scripts=['cliparser/accolade'], install_requires= ['boto3', 'botocore', 'pipdate'])
