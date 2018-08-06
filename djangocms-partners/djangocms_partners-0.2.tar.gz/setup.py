import os
from setuptools import setup, find_packages

def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangocms_partners',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='BSD 3-Clause "New" or "Revised" License',
    description='show parteners',
    long_description=read('README.md'),
    url='https://github.com/dmodules/djangocms_partners',
    author='D-Modules',
    #install_requires=["django-taggit==0.22.1"],
    author_email='support@d-modules.com',
)
