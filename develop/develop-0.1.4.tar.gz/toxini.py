# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

"""
this is for writing the tox.ini file dynamically based on information
in __init__.py->_package_data

Need to be able to write two different versions, because vboxsf filesystems
do not allow hardlinking, and tox/virtualenv use that.

So a version with toxworkdir is written before actual testing and one with that
line commented out before commit.

Could put alternate `tox.ini`` in `/data1/DATA/tox/ruamel.yaml``, but that would
mean invocation with `tox -c` even after `dv --keep`.


If the 'dev' entry for tox has comma, the string is taken as-is and a trailing comma
is replaced. Otherwise the string is interpreted:

   dev='py37,py36' -> select python 3.7 and 3.6 as targets
   dev='py36,' -> only select Python 3.6 as target
   dev='py36' -> assertion error (based on the 'y')
   dev='*' -> all active python
   dev='32pjn' -> 3: latest released 3.X.Y, 2: latest released 2.7.X,
                  p: pypy, j: jython, n: narrow 2.7 build

"""

from ruamel.std.pathlib import Path


VER2 = ['py27']
VER3 = ['py37', 'py36', 'py35', 'py34']


class ToxIni:
    def __init__(self, settings, work_dir='.', sub_packages=None):
        self._tox_settings = settings
        self._work_dir = work_dir
        self._sub_packages = sub_packages
        self._path = Path('tox.ini')

    def write(self, work_dir=True):
        twd = ("" if work_dir else '# ') + 'toworkdir'
        narrow = False
        with self._path.open('w') as fp:
            code_style = 'cs'  # pep8
            print('[tox]', file=fp)  # NOQA
            print(f'{twd} = {self._work_dir} ', file=fp)  # NOQA
            envlist = [code_style]
            e = str(self._tox_settings['env'])
            # env 3 -> latest 3, 2 -> latest 2, * all active, p -> pypy, j -> jython
            if ',' in e:
                if e[-1] == ',':
                    e = e[:-1]
                envlist = [e]
            else:
                assert 'y' not in e, 'You probably want to put a comma in the tox.dev spec'
                if '3' in e:
                    envlist.append(VER3[0])
                if '2' in e:
                    envlist.append(VER2[0])
                if '*' in e:
                    # to get errors depending on major version differeces quicker
                    envlist.extend([VER3[0], VER2[0]] + VER3[1:] + VER2[1:])
                if 'p' in e:
                    envlist.append('pypy')
                if 'n' in e:
                    narrow = True
                    envlist.append(VER2[0] + 'm')
                if 'j' in e:
                    envlist.append('jython')

            print('envlist = {}'.format(','.join(envlist)), file=fp)
            print('\n[testenv]', file=fp)
            print('commands =', file=fp)
            # print('''    python -c "import sys, sysconfig; print('%s ucs-%s' % '''
            #       '''(sys.version.replace('\\n', ' '), sysconfig.get_config_var'''
            #       '''('Py_UNICODE_SIZE')))"''', file=fp)
            print("    /bin/bash -c 'pytest _test/test_*.py'", file=fp)
            print('deps =', file=fp)
            # deps extra dependency packages for testing
            deps = ['pytest']
            tdeps = self._tox_settings.get('deps', [])
            if isinstance(tdeps, str):
                deps.extend(tdeps.split())
            else:
                deps.extend(tdeps)
            for dep in deps:
                print('    {}'.format(dep), file=fp)
            if narrow:
                pyver = '/opt/python/2.7.15m'  # could be dynamic
                print(f'\n[testenv:py27m]\nbasepython = {pyver}/bin/python', file=fp)
            # [pytest]
            # norecursedirs = test/lib .tox
            deps = []
            flake8ver = self._tox_settings.get('flake8', {}).get('version', "")
            if flake8ver:
                deps.append('flake8' + flake8ver)  # probably 2.5.5
            else:
                # bug-bear need flake8>3, so probably no version allowed
                deps.extend(['flake8', 'flake8-bugbear;python_version>="3.5"'])
            # pep8 for muscle-memory
            for cs in [code_style, 'pep8']:
                print('\n[testenv:{}]'.format(cs), file=fp)
                print('basepython = python3.6', file=fp)
                print('deps =', file=fp)
                for dep in deps:
                    print('    {}'.format(dep), file=fp)
                print('commands =', file=fp)
                subdirs = []
                # subdirs = [".tox", ".#*"]
                # fl8excl extra dirs for exclude
                if subdirs:
                    subdirs = ' --exclude "' + ','.join(subdirs) + '" '
                # print('    python -c "import os; print(os.getcwd())"', file=fp)
                print('    flake8 {}{{posargs}}'.format(subdirs), file=fp)
            print('\n[flake8]', file=fp)
            print('show-source = True', file=fp)
            print('max-line-length = 95', file=fp)
            # the following line was in tox.ini for pon E251 is space around keyword?
            # print('ignore = E251', file=fp)
            flake8_ignore = dict(
                W503='line break before binary operator',
                F405='undifined name ( from x import * )',
                E203='whitespace before ":"',
            )
            print('ignore = {}'.format(','.join(flake8_ignore.keys())), file=fp)
            excl = self._tox_settings.get('fl8excl', "")
            if excl and isinstance(excl, str):
                excl = ','.join(excl.split()) + ','
            elif excl:
                excl = ','.join(excl) + ','
            if self._sub_packages:
                subdirs.extend(self._sub_packages)
            print(
                'exclude = {}.hg,.git,.tox,dist,.cache,__pycache__,'
                'ruamel.zip2tar.egg-info'.format(excl),
                file=fp,
            )
            print('\n[pytest]', file=fp)
            print('filterwarnings =', file=fp)
            print('    error::DeprecationWarning', file=fp)
            print('    error::PendingDeprecationWarning', file=fp)
        if work_dir:
            self._path.copy(self._work_dir)  # for review purposes

    def prepare_commit(self):
        self.write(work_dir=False)
