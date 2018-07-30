# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sphinxience']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=1.7,<1.8']

setup_kwargs = {
    'name': 'sphinxience',
    'version': '0.1.2a0',
    'description': 'A Sphinx extension to assist in publishing scientific writing in either HTML or PDF.',
    'long_description': '# Sphinxience\n\nA Sphinx extension to assist in publishing scientific writing in either HTML or PDF. \n\nThis extension mainly consists of a number of roles and directives, so that you can use most LaTeX macros more easily than writing inline LaTeX in Sphinx. This extension will also monkeypatch your HTML theme and LaTeX settings, to make the LaTeX output conform to what is expected of scientific papers submitted to conferences/journals.\n\nSphinxience is pronounced either like "Sphinx science" or rhyming with "experience". It\'s up to you.\n\nTODO **Warning: This package is still a dummy; I\'m in the (slow) process of open sourcing this.**',
    'author': 'Bram Geron',
    'author_email': 'bram@bram.xyz',
    'url': 'https://github.com/bgeron/sphinxience',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
