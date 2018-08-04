# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name=u'develop',
    version_info=(0, 1, 4),
    __version__='0.1.4',
    author=u'Anthon van der Neut',
    author_email=u'a.van.der.neut@ruamel.eu',
    description=u'tool to develop python packages',
    # keywords="",
    entry_points=u'dv=develop.__main__:main',
    # entry_points=None,
    license=u'MIT',
    since=2017,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    # universal=True,
    install_requires=[
            u'ruamel.appconfig',
            u'ruamel.showoutput',
            u'ruamel.std.argparse>=0.8',
            u'python-hglib',
            u'repo',
            u'readme-renderer',
    ],
    tox=dict(
        env=u'3',
    ),
    pre_black=True,
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']
