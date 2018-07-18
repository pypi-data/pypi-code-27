# pylint: disable=W0622
"""cubicweb-pwd-policy application packaging information"""


modname = 'cubicweb_pwd_policy'
distname = 'cubicweb-pwd-policy'

numversion = (1, 0, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Password policy for cubicweb applications'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {'cubicweb': '>= 3.24.7', 'six': '>= 1.4.0'}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
