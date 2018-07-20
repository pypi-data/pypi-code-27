# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tensionflow', 'tensionflow.datasets', 'tensionflow.model']

package_data = \
{'': ['*']}

install_requires = \
['bidict>=0.14,<0.15',
 'click>=6.7,<7.0',
 'librosa>=0.6,<0.7',
 'llvmlite>=0.24.0,<0.25.0',
 'numpy>=1.14,<2.0',
 'pandas>=0.23,<0.24',
 'tensorflow>=1.8,<2.0',
 'typing>=3.6,<4.0']

entry_points = \
{'console_scripts': ['tensionflow = tensionflow.cli:cli']}

setup_kwargs = {
    'name': 'tensionflow',
    'version': '0.1.0',
    'description': 'A Tensorflow framework for working with audio data.',
    'long_description': '# Tensionflow\n\n[![Build Status](https://travis-ci.org/Curly-Mo/tensionflow.svg?branch=master)](https://travis-ci.org/Curly-Mo/tensionflow)\n[![Coverage](https://coveralls.io/repos/github/Curly-Mo/tensionflow/badge.svg)](https://coveralls.io/github/Curly-Mo/tensionflow)\n[![Documentation](https://readthedocs.org/projects/tensionflow/badge/?version=latest)](https://tensionflow.readthedocs.org/en/latest/?badge=latest)\n[![PyPI](https://img.shields.io/pypi/v/tensionflow.svg)](https://pypi.python.org/pypi/tensionflow)\n[![PyPI Pythons](https://img.shields.io/pypi/pyversions/tensionflow.svg)](https://pypi.python.org/pypi/tensionflow)\n[![License](https://img.shields.io/pypi/l/tensionflow.svg)](https://github.com/Curly-Mo/tensionflow/blob/master/LICENSE)\n\nA Tensorflow framework for working with audio data.\n\n## Features\n\n* TODO\n\n## Usage\n\n* TODO\n\n## Install\n\n```console\npip install tensionflow\n```\n\n## Documentation\nSee https://tensionflow.readthedocs.org/en/latest/\n\n## Development\n```console\npip install poetry\ncd tensionflow\npoetry install\n```\n### Run\nTo run cli entrypoint:\n```console\npoetry run tensionflow --help\n```\n\n### Tests\n```console\npoetry run tox\n```\n\n### Docker\nTo run with docker\n```console\ndocker build -t tensionflow .\ndocker run tensionflow:latest tensionflow --help\n```\n\n## License\n[LGPL-3.0](https://github.com/Curly-Mo/tensionflow/blob/master/LICENSE)\n',
    'author': 'Colin Fahy',
    'author_email': 'colin@cfahy.com',
    'url': 'https://github.com/Curly-Mo/tensionflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
