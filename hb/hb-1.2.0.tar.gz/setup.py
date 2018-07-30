# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hb']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7,<7.0']

entry_points = \
{'console_scripts': ['hb = hb.cli:cli']}

setup_kwargs = {
    'name': 'hb',
    'version': '1.2.0',
    'description': 'A simple command-line utility for calculating checksums.',
    'long_description': '# Hash Brown\n\n[![CircleCI](https://circleci.com/gh/chingc/Hash-Brown.svg?style=shield)](https://circleci.com/gh/chingc/workflows/Hash-Brown) [![codecov](https://codecov.io/gh/chingc/Hash-Brown/branch/master/graph/badge.svg)](https://codecov.io/gh/chingc/Hash-Brown) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![PyPI](https://img.shields.io/pypi/v/hb.svg)](https://pypi.org/project/hb/)\n\nA simple command-line utility for calculating checksums.\n\n## Install\n\n```\npip install hb\n```\n\n## Usage\n\nCalculate the sha1 of a file:\n\n```\n$ hb -a sha1 hello.txt\nsha1 (hello.txt) = 493a253abf93d705d67edeb463134a5c8752fc9d\n```\n\nCheck to see if file matches a given checksum:\n\n```\n$ hb -a md5 hello.txt -g 77060c267470021a97392b815138733e\nmd5 (hello.txt) = 77060c267470021a97392b815138733e OK\n\n$ hb -a md5 hello.txt -g 0123456789abcdef\nmd5 (hello.txt) = 0123456789abcdef ACTUAL: 77060c267470021a97392b815138733e\n```\n\nChecksums can be read from a file:\n\n```\n$ hb -c checksums.txt\nsha512 (hello.txt) = 493a253abf93d705d67edeb463134a5c8752fc9d OK\nsha512 (world.txt) = 683e4ee04e75e71a6dca42807001f00be1fcb2a3 OK\nsha512 (image.jpg) = f3a53e6c2743645f08faedadd7a2c57cbc38632f OK\nsha512 (video.mp4) = 03ba9191fc4cd74f218df58542643fbc07dca532 OK\n```\n\nHash Brown outputs its results in BSD style.  The checksum files are also BSD style.\n\nAll files are read in binary mode.\n\nGlobbing and recursive globbing are supported via `*` and `**` respectively.\n\nDotfiles are not included when globbing and need to be specified explicitly.\n\n## Options\n\n```\n-a, --algorithm [blake2b|blake2s|md5|sha1|sha224|sha256|sha384|sha512|adler32|crc32]\n-c, --check                     Read checksums from a file.\n-g, --given TEXT                See if the given checksum `TEXT` matches the\n                                computed checksum. (use with -a)\n--version                       Show the version and exit.\n-h, --help                      Show this message and exit.\n```\n',
    'author': 'Ching Chow',
    'author_email': 'ching.chow.sc@gmail.com',
    'url': 'https://github.com/chingc/Hash-Brown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
