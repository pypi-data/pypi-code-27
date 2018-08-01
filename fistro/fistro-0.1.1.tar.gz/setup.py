# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fistro']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fistro',
    'version': '0.1.1',
    'description': 'A fixture generator based on type annotations.',
    'long_description': 'Fistro\n======\n\n.. image:: https://img.shields.io/pypi/v/fistro.svg\n    :target: https://pypi.org/project/fistro/\n\n.. image:: https://img.shields.io/pypi/pyversions/fistro.svg\n    :target: https://pypi.org/project/fistro/\n\n.. image:: https://img.shields.io/circleci/project/github/kingoodie/fistro.svg\n    :target: https://circleci.com/gh/kingoodie/fistro\n\n.. image:: https://codecov.io/gh/kingoodie/fistro/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/kingoodie/fistro\n\nA fixture generator based on type annotations.\n\nExamples\n--------\n\n>>> from datetime import datetime, date\n>>>\n>>> from fistro.fistro import generate\n>>>\n>>>\n>>> class Employee:\n>>>     id: int\n>>>     name: str = \'Carlos SÃ¡nchez\'\n>>>     birthday: date\n>>>     last_access: datetime\n>>>     password: str\n>>>\n>>>\n>>> employee = generate(Employee)()\n>>> print(employee)\n\nIt will show something like this:\n\n>>> Employee(id=7621035066, name=\'Carlos SÃ¡nchez\', birthday=datetime.date(259, 2, 21), last_access=datetime.datetime(2190, 11, 7, 7, 3, 20), password=":F\'5nr\\x0ch~")\n\n\nInstallation\n------------\n\n>>> pip install fistro\n\n\nCredits\n--------\nIn memoriam of `Chiquito de la Calzada <https://es.wikipedia.org/wiki/Chiquito_de_la_Calzada>`_.',
    'author': 'Pablo Cabezas',
    'author_email': 'pabcabsal@gmail.com',
    'url': 'https://github.com/kingoodie/fistro',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<3.8.0',
}


setup(**setup_kwargs)
