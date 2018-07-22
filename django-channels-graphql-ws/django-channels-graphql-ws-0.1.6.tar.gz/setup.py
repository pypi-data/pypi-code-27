# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['channels_graphql_ws']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=2.3,<3.0',
 'channels>=2.1,<3.0',
 'django>=2.0,<3.0',
 'graphene>=2.1,<3.0',
 'graphene_django>=2.0,<3.0',
 'graphql-core>=2.0,<3.0',
 'namedlist>=1.7,<2.0',
 'rx>=1.6,<2.0']

setup_kwargs = {
    'name': 'django-channels-graphql-ws',
    'version': '0.1.6',
    'description': 'Django Channels based WebSocket GraphQL server with Graphene-like subscriptions',
    'long_description': None,
    'author': 'Alexander A. Prokhorov',
    'author_email': 'alexander.prokhorov@datadvance.net',
    'url': 'https://github.com/datadvance/DjangoChannelsGraphqlWs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
