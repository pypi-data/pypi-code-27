# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mullvad_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7,<7.0', 'colorama>=0.3.9,<0.4.0', 'requests>=2.19,<3.0']

entry_points = \
{'console_scripts': ['mullpy = mullvad_python.cli:main']}

setup_kwargs = {
    'name': 'mullvad-python',
    'version': '0.1.1',
    'description': 'Check Mullvad VPN connection status.',
    'long_description': "# Mullpy\n\nA little script to check if you're currently connected to **Mullvad** VPN or not. Read the _very flattering_ [Mullvad review here](https://thatoneprivacysite.net/2017/10/03/mullvad-review/) by [That One Privacy Site](https://thatoneprivacysite.net/)\n\n\n# Installation\n\n**Requirements:**\n* Python 3.6 and up.\n\n**Instalation vía Pip:**\n```bash\n$ pip install --user mullvad-python\n```\n",
    'author': 'Franccesco Orozco',
    'author_email': 'franccesco.orozco@codingdose.info',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
