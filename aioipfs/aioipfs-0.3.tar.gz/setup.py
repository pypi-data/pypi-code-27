
import os, os.path, re
import sys
import codecs
from setuptools import setup, find_packages

PY_VER = sys.version_info

if PY_VER >= (3, 5):
    pass
else:
    raise RuntimeError("You need python3.5 or newer")

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'aioipfs', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='aioipfs',
    version=version,
    license='GPL3',
    author='David Ferlier',
    url='https://gitlab.com/cipres/aioipfs',
    description='Asynchronous IPFS client library',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=['aioipfs', 'scripts'],
    include_package_data=False,
    install_requires=[
        'aiohttp>=2.0.0',
        'aiofiles',
        'async_generator>=1.0',
        'yarl',
        'base58',
        'tqdm'
        ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: System :: Filesystems',
    ],
    entry_points={
        'console_scripts': [
            'asyncipfs = scripts.asyncipfs:start',
            'ipfs-find = scripts.ipfsfind:start'
        ]
    },
    keywords=[
        'asyncio',
        'aiohttp',
        'ipfs'
    ],
)
