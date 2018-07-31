
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
import os

from glob import glob

import publicize

modules = glob('*.py')

file = os.path.normcase(publicize.__file__)
pub_wd, pub_fp = os.path.split(file)
cwd = os.path.normcase(os.getcwd())

if pub_wd != cwd:
    
    with open(file, 'rb') as fp:
        print('reading from:', file)
        src = fp.read()
        
    with open(os.path.join(cwd, pub_fp), 'wb') as fp:
        print('writing to:', os.path.join(cwd, pub_fp))
        fp.write(src)

print('version is', publicize.__version__)
print('file is', publicize.__file__)
##
publicize_classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 2",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

if 1:
    with open('README.rst') as fp:
        setup(name="publicize",
              version=publicize.__version__,
              author="Dan Snider",
              author_email='dan.snider.cu@outlook.com',
              url="http://pypi.python.org/pypi/publicize/",
              py_modules=["publicize"],
              description="Utilities to manage the way a module is exported",
              license="MIT",
              classifiers=publicize_classifiers,
              long_description=fp.read()
              )
