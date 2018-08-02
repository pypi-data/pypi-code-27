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
    'version': '0.3.0',
    'description': 'Check Mullvad VPN connection status.',
    'long_description': '# Mullpy\n[![Build Status](https://travis-ci.org/franccesco/mullpy.svg?branch=master)](https://travis-ci.org/franccesco/mullpy) [![Coverage Status](https://coveralls.io/repos/github/franccesco/mullpy/badge.svg?branch=develop)](https://coveralls.io/github/franccesco/mullpy?branch=develop)\n\nA little tool to check if you\'re currently connected to **Mullvad** VPN or not. Read the _very flattering_ [Mullvad review here](https://thatoneprivacysite.net/2017/10/03/mullvad-review/) by [That One Privacy Site](https://thatoneprivacysite.net/)\n\nThe tool _does not_ intend to be a swiss army knife, just a weekend mini project so I don\'t have to go to [am.i.mullvad.net](http://am.i.mullvad.net/) everytime to check on my connection. **For WebRTC and DNS leaks you should go to their website!**\n\n![Mullvad ON](assets/mullvad_on.png)\n\n# Installation\n\n**Requirements:**\n* Python 3.6 and up.\n\n**Instalation vía Pip:**\n```bash\n$ pip install --user mullvad-python\n```\n\n# Usage\n```\n$ mullpy\n   \\  |         |  |               \n  |\\/ |  |   |  |  |  __ \\   |   | \n  |   |  |   |  |  |  |   |  |   | \n _|  _| \\__,_| _| _|  .__/  \\__, | \n                     _|     ____/  \n\nUsing Mullvad:\tTrue\nServer Type:\tWireguard\nIP Address:\t185.232.22.59\nCountry:\tNew York, United States\nLocation:\t-74.0052, 40.7214\nOrganization:\tM247 Europe SRL\nBlacklisted: \tFalse\n```\n\n# TODO\n- [x] CLI\n- [x] Testing\n- [x] Continuous Integration\n- [x] Code Coverage\n- [ ] Port Checking\n- [ ] DNS Leak Test\n- [ ] Verbose options\n\n\n# Support this project\nIf you like the project and would like to support me you can buy me a cup of coffee, that would be much appreciated 🙏. If you can\'t, don\'t worry, enjoy it :)\n\n<a href="https://www.paypal.me/orozcofranccesco">\n  <img height="32" src="assets/paypal_badge.png" />\n</a> <a href="https://www.buymeacoffee.com/franccesco" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a> <a href=\'https://ko-fi.com/V7V8AXFE\' target=\'_blank\'><img height=\'36\' style=\'border:0px;height:36px;\' src=\'https://az743702.vo.msecnd.net/cdn/kofi2.png?v=0\' border=\'0\' alt=\'Buy Me a Coffee at ko-fi.com\' /></a>\n',
    'author': 'Franccesco Orozco',
    'author_email': 'franccesco.orozco@codingdose.info',
    'url': 'https://github.com/franccesco/mullpy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
