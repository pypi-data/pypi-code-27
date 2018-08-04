# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

"""
develop (dv, dvm, dvt) is a wrapper around programs like hg,
make, tox, pytest, devpi, flask8, etc that creates "missing" files
from information in __init__.py, then runs the program and deletes
those "missing" files. It prevents clutter and single source
configuration.

It replaces several options that were only

- Makefile doesn't need to get version using "python setup.py --version", which is slow

ToDo:
- more intelligent pushing of dist files to other servers

"""

import datetime
import io
import os
import subprocess
import sys
import time  # NOQA
from datetime import date
from textwrap import dedent
from contextlib import ContextDecorator

from pon import PON
from ruamel.std.pathlib import Path, pushd, popd
from ruamel.showoutput import show_output
from .readme import ReadMe
from .toxini import ToxIni
from .ununinit import ununinitpy, version_init_files, set_dev
from .hgignore import dot_hgignore, HgIgnore, GlobalHgIgnore

versions = {
    'py26': [9, date(2013, 10, 29)],
    'py27': [13, None],
    'py30': [1, date(2009, 2, 13)],
    'py31': [
        5,
        date(2012, 6, 30),
        'https://www.python.org/dev/peps/pep-0375/#maintenance-releases',
    ],
    'py32': [7, date(2016, 2, 28), 'https://www.python.org/dev/peps/pep-0392/#lifespan'],
    'py33': [7, date(2017, 9, 30), 'https://www.python.org/dev/peps/pep-0398/#lifespan'],
    'py34': [6, None, 'https://www.python.org/dev/peps/pep-0429/'],
    'py35': [3, None, 'https://www.python.org/dev/peps/pep-0478/'],
    'py36': [1, None, 'https://www.python.org/dev/peps/pep-0494/'],
}


mit_license = """\
 The MIT License (MIT)

 Copyright (c) {year} {fullname}

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""


class TmpFiles(ContextDecorator):
    def __init__(
        self, parent, setup=True, license=True, tox=None, makefile=False, sub_packages=None
    ):
        self._rm_after = []
        self.parent = parent
        self.setup = setup
        self.license = license
        self.tox = tox
        self.makefile = makefile
        self.sub_packages = sub_packages
        self.keep = parent._args.keep
        self.pon = self.parent.pon  # trigger any check on pon
        self._toxini = None  # keep in case of .prepare_commit

    def __enter__(self):
        if self.setup:
            src = Path('~/.config/develop/dv_setup.py').expanduser()
            p = Path('setup.py')
            if not p.exists():
                src.copy(p)
            self._rm_after.append(p)
        if self.license:
            lic = self.pon.obj.get('license')
            if lic is None or 'MIT' in lic:
                plic = Path('LICENSE')
                start_year = self.pon.obj['since']  # has to be in __init__.py
                this_year = date.today().year
                if start_year != this_year:
                    year = '{}-{}'.format(start_year, this_year)
                else:
                    year = this_year
                plic.write_text(
                    mit_license.format(year=year, fullname='Anthon van der Neut, Ruamel bvba')
                )
                self._rm_after.append(plic)
        _tox = self.pon.obj.get('tox')
        if self.tox is not None and _tox is None:
            print('no tox specification in __init__.py')
        # print('tox:', _tox)
        if self.tox is not None and _tox is not None:
            # print('subpackages', self.sub_packages)
            # sys.stdout.flush()
            self._tox_ini = ToxIni(_tox, work_dir=self.tox, sub_packages=self.sub_packages)
            self._tox_ini.write()
            self._rm_after.append(self._tox_ini._path)
        if self.makefile:
            fpn = self.pon.obj['full_package_name']
            util_name = fpn.rsplit('.', 1)[-1]
            version = self.pon.obj['__version__']
            versiond = version + '0' if version.endswith('.dev') else version
            m = Path('.Makefile.tmp')
            if False:
                mt = Path('Makefile.tmp')
                if m.exists() and not mt.exists():
                    m.rename(mt)
            with m.open('w') as fp:
                print(f'\nUTILNAME:={util_name}', file=fp)
                print(f'PKGNAME:={fpn}', file=fp)
                print(f'INSTPKGNAME:=--pkg {fpn}', file=fp)
                print(f'VERSION:={version}', file=fp)
                print(f'VERSIOND:={versiond}', file=fp)
                # print('\ninclude ~/.config/ruamel_util_new/Makefile.inc', file=fp)
                print('\ninclude ~/.config/develop/Makefile.inc', file=fp)
                # print('\nclean: clean_common', file=fp)  # replaced by dv clean
            self._rm_after.append(m)
        return self

    def __exit__(self, typ, value, traceback):
        if typ:
            print('typ', typ)
        if self.keep:
            return
        for p in self._rm_after:
            p.unlink()

    def prepare_commit(self):
        """prepare any files for committing"""
        if self._tox_ini:  # only set if generated, not when available
            self._tox_ini.prepare_commit()


class DevelopError(Exception):
    pass


class Log:
    def __init__(self):
        pass

    def __enter__(self):
        print('__enter__')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__')


PKG_DATA = '_package_data'


class Develop:
    def __init__(self, args, config):
        self._args = args
        self._config = config
        self.do_tag = True
        self.old_dist_dir = Path('dist')
        self.old_tox_dir = Path('.tox')
        self.readme_file = Path('README.rst')
        self._readme = ReadMe('README.rst')
        if False:
            for line in self._readme.lines[12:20]:
                print('>', line)
            print('idx', self._readme.find_single_line_starting_with('  - add'))
        self.commit_message_file = Path('.hg/commit_message.txt')
        self.docker_file = Path('Dockerfile')
        self._version = None
        self._version_s = None

    def repo_status(self):
        """check various stati related to versioning/packaging"""
        from repo.status import unclean_list, check_output

        if self._args.verbose > 0:
            print('check repo status', end=' ')
            sys.stdout.flush()
        ok = True
        # status of the repository
        lst = unclean_list()
        if lst:
            ok = False
            if self._args.verbose > 0:
                print('-> NOT ok')
            print('repo will not be clean after commit')
            for k in lst:
                print(' ', k)
        branch = check_output(['hg', 'branch']).strip()
        if branch != 'default':
            if self._args.verbose > 0:
                print('-> NOT ok')
            ok = False
            print('not on default branch [{}]'.format(branch))
        # the following is not enough for a readme check, e.g on "`Anthon <>`__"
        res = check_output(
            [
                '/home/venv/dev/bin/python',
                'setup.py',
                'check',
                '--strict',
                '--restructuredtext',
                '--metadata',
            ]
        ).rstrip()
        if not self._args.test and res != 'running check':
            if self._args.verbose > 0:
                print('-> NOT ok')
            print('running check: [{}]'.format(res))
            ok = False
        if ok and self._args.verbose > 0:
            print('-> ok')
        return ok

    def readme_check(self):
        from io import StringIO
        from readme_renderer import rst

        ok = True
        if self._args.verbose > 0:
            print('checking {}'.format(self.readme_file), end=' ')
            sys.stdout.flush()
        warnings = StringIO()
        text = self.readme_file.read_text()
        if '\n\nNEXT:' not in text and 'ChangeLog' in text:
            if ok:
                print('-> NOT ok')
            print('develop: NEXT: not found')
            ok = False
        out = rst.render(text, stream=warnings)
        if out is None:
            if ok:
                print('-> NOT ok')
            print(warnings.getvalue())
            ok = False
        if ok and self._args.verbose > 0:
            print('-> ok')
        return ok

    @property
    def pon(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            pon = PON()
            try:
                with io.open(ununinitpy) as fp:
                    if pon.extract(fp, start=PKG_DATA) is None:
                        print('not extracted', ununinitpy, PKG_DATA)
                        pon = None
                    else:
                        check_init_pon(ununinitpy, pon)
            except FileNotFoundError:
                d = os.getcwd()
                print(f'no {ununinitpy} found in {d}')
                sys.exit(-1)
            setattr(self, attr, pon)
        return getattr(self, attr)

    def tox(self):
        tox_wd = self.check_tox_dir()
        with TmpFiles(self, tox=tox_wd, sub_packages=self.sub_packages):
            try:
                args = self._args.args
                cmd = ['detox']
                if self._args.e:
                    cmd = ['tox']
                    args = ['-e', self._args.e] + args
                if self._args.r:
                    args = ['-r'] + args
                res = show_output(cmd + args, show_command=True)
            except subprocess.CalledProcessError:
                return
            print('res:', res)

    def mypy(self):
        # we could have files in subdirectories that need inclusion, and
        # for that you have to walk the subtree, skip any sub-packages
        # base on their __init__.py:_package_data['nested']
        # for now (ruamel.yaml) solve as the Makefile did
        # MYPYSRC:=$(shell ls -1 *.py | grep -Ev "^(setup.py|.*_flymake.py)$$" | \
        #    sed 's|^|ruamel/yaml/|')
        # MYPYOPT:=--py2 --strict --follow-imports silent
        #
        # mypy:
        #       @echo 'mypy *.py'
        #       @cd ../.. ; mypy $(MYPYOPT) $(MYPYSRC)
        #       mypy $(MYPYOPT) $(MYPYSRC1)
        res = None
        options = ['--py2', '--strict', '--follow-imports', 'silent']
        fpn_split = self.pon.obj['full_package_name'].split('.')
        _root_dir = '/'.join(['..'] * len(fpn_split))
        pushd(_root_dir)
        pkg_path = Path('/'.join(fpn_split))
        files = []
        for path in pkg_path.glob('*.py'):
            if path.name.startswith('.#'):
                continue
            if path.name == 'setup.py':  # might not be there
                continue
            if path.stem.endswith('_flymake'):
                continue
            files.append(path)
            # print(' ', path)
        # print(len(files))
        try:
            res = show_output(['mypy'] + options + files, verbose=True, show_command='\\')
        except subprocess.CalledProcessError as e:
            pass
        if res:
            print(res)
        popd()

    def make(self):
        try:
            util_name = self.pon.get('util')
            if util_name:
                os.environ['OPTUTILNAME'] = util_name
        except KeyError:
            pass
        try:
            entry_points = self.pon.get('entry_points')  # NOQA
        except KeyError:
            pass
        self.check_dist_dir()
        self.use_alternative('clean')
        with TmpFiles(self, makefile=True, sub_packages=self.sub_packages):
            if self._args.args:
                try:
                    res = show_output(['make', '-f', '.Makefile.tmp'] + self._args.args)
                    res = None  # NOQA
                except subprocess.CalledProcessError:
                    sys.exit(0)

    def use_alternative(self, alternatives):
        if not isinstance(alternatives, list):
            alternatives = [alternatives]
        try:
            arg0 = self._args.args[0]
        except IndexError:
            return None
        if arg0 and arg0 in alternatives:
            print('Use:\n   dv {}\n.'.format(self._args.args[0]))
            sys.exit(1)
        return False

    def version(self):
        """
        this currently directly calls the various (package)version commands
        (-> direct dv replacement if available):

        show                show current version
        bump                bump version number if equal to latest on PyPI
        major               bump minor version number
        minor               bump minor version number
        micro               bump micro version number
        dev                 set/unset dev
        update              update to preferred __init__.py etc
        license             update license info
        status              check status of project
        push                check, commit, push, upload and bump if everything ok
        bitbucket           create/check bitbucket
        test                test package setup (conformity, pypi, bitbucket)

        "dvv" equals "dv version" use "dvv -- push --reuse --no-tox" to end commandline
        interpretation
        """
        if self._args.badge:
            return self.version_badge(force=True)
        if self._args.args and self._args.args[0] == 'push':
            print('Use:\n   dv {}\n'.format(self._args.args[0]))
            # with TmpFiles(self, license=True, tox=True, makefile=True):
            #     self.do_version()
            return
        self.do_version()

    def version_badge(self, version=None, include_dev=False, force=False, text_badge='pypi'):
        """if not fore just try to find, but don't error if you can't

        Need to test with firefox/chrome as eog does not use all .svg stuff (textwidth!)
        """
        badge = Path('_doc/_static/{}.svg'.format(text_badge))
        if force:
            assert badge.is_file()
        text = badge.read_text()
        if '{version}' in text:
            text = text.replace('{version}', '1.2.3')
        if version is None:
            with io.open(ununinitpy) as fp:
                pon = PON()
                pon.extract(fp, start=PKG_DATA)
                version = pon.obj.get('__version__')
                if not include_dev:
                    version = version.replace('.dev', "")
        split = text.split('</text>')
        old_version = None
        for idx, s in enumerate(split):
            if s.endswith('>' + text_badge):
                continue
            base, end = s.rsplit('>', 1)
            if not end.strip():
                continue
            # print('base end', repr(end))
            if old_version is None:
                old_version = end
            else:
                assert (
                    old_version == end
                ), f'different versions in {text_badge} badge: "{old_version}" and "{end}"'
            split[idx] = base + '>' + version
            if old_version and old_version == end:
                text = '</text>'.join(split)
                badge.write_text(text)
            else:
                print('no version to replace found')
        # Maybe also need to set the last two textlengths

        # print(text.replace('>', '>\n'))
        # print('--- done')

    def clean(self):
        cmds = [
            'rm -rf build .tox {}.egg-info/ README.pdf _doc/*.pdf _doc/_build'.format(
                self.pon.obj['full_package_name']
            ),
            'find . -name "*.pyc" -exec rm {} +',
            'find . -name "*~" -exec rm {} +',
            'find . -name "*.orig" -exec rm {} +',
            'find . -name "__pycache__" -print0  | xargs -r -0 rm -rf',
        ]
        for cmd in cmds:
            print(cmd)
            os.system(cmd)

    def rtfd(self):
        if self._args.build:
            prj = self.pon.obj['read_the_docs']
            os.system('curl -X POST https://readthedocs.org/build/{}'.format(prj))
            return
        print('rtfd what?')

    def environment_sane(self):
        """
        here the environment is checked and the version number retrieved
        """
        import hglib

        ok = []
        if not self.devpi_logged_in():
            ok.append('devpi_logged_in')
        # get latest version from hg history? and check if __init__ has been updated.
        client = hglib.open('.')
        for tag, _change, _hash, _local in client.tags():
            if tag == b'tip':
                continue
            committed_version = [
                int(i) if i[0].isalnum() else i for i in tag.decode('utf-8').split('.')
            ]
            # tag = tag.decode('utf-8').split('.')
            print('committed_version', committed_version)
            break

        if False:
            print('ok:', ok)
            print(self._args.from_develop)
            print()
            return
        for idx, (file_name, version, comment) in enumerate(version_init_files('.')):
            if idx != 0:  # there can be only one
                ok.append('version_init_file {} found'.format(file_name))
                break
            assert comment == ""
            if self._args.verbose > 0:
                print('filename', file_name)
            print('version', version)
            assert 'dev' in version
        self._version = version[:3]
        self._version_s = '.'.join([str(t) for t in self._version])
        # if self._args.changestest:
        #    self.check_update_readme(version, testing=True)
        #    return
        if not self.check_nested():
            ok.append('check_nested')
        if not self.readme_check():
            ok.append('readme')
        if not self.repo_status():
            ok.append('status')
        if ok != []:
            print('not ok', ok)
            return False
        if not self.flake_it():
            ok.append('flake_it')
        if ok != []:
            print('not ok', ok)
            return False
        return True

    def flake_it(self):
        try:
            show_output(['flake8'])
        except Exception as e:
            return False
        return True

    def check_commit_message_file(self):
        """
        check if commit message exists, if not create it, edit and strip
        stripping is necessary because --logfile doesn't do this
        """
        try:
            text = self._args.commit_message
            return True
        except AttributeError:
            pass
        if self._args.reuse_message:
            if not self.commit_message_file.exists():
                print(
                    "reuse specified but {} doesn't exist. do:\n\n{}\n".format(
                        self.commit_message_file,
                        '    cp -i .hg/last-message.txt .hg/commit_message.txt',
                    )
                )
                return False
            return True
        try:
            self.commit_message_file.unlink()
        except OSError:
            pass
        old_env = os.environ.get('EDITOR')
        os.environ['EDITOR'] = 'ex'
        os.system('echo "wq {}" | hg commit 2>/dev/null'.format(self.commit_message_file))
        if old_env is None:
            del os.environ['EDITOR']
        else:
            os.environ['EDITOR'] = 'ex'
        # Now done in ~/.hgrc
        # txt = self.commit_message_file.read_text()
        # txt.replace('HG:', 'HG: Please close this issue if you can confirm it solves'
        #             ' the reported problem\n\n', 1)

        raise NotImplementedError
        # self.commit_message_file.write_text(txt)
        # print('txt\n', txt)
        # os.system('vi {}'.format(self.commit_message_file))
        text = ""
        with self.commit_message_file.open() as fp:
            for line in fp:
                if line.startswith('HG:'):
                    continue
                text += line
        text = text.strip()  # removes trailing empty lines
        if text == "":
            print('error: empty message file', self.commit_message_file)
            self.commit_message_file.unlink()
            return False
        text += '\n'
        self.commit_message_file.write_text(text)
        return True

    @property
    def nested(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, self.pon.obj.get('nested'))
        return getattr(self, attr)

    def check_nested(self):
        """check if there is a parent __init__.py file that is just for commits
        in that case `nested=True,` should be in the package data
        """
        if self._args.verbose > 0:
            print('checking if nested', end=' ')
            sys.stdout.flush()
        if self.nested:
            if self._args.verbose > 0:
                print('-> ok')
            return True
        parent_init_py = Path('..') / ununinitpy
        if '_package_data = dict' not in parent_init_py.read_text():
            if self._args.verbose > 0:
                print('-> ok')
            return True
        if self._args.verbose > 0:
            print('-> NOT ok')
        print(f'this is a nested package, but "nested=True" is not in {ununinitpy}')
        return False

    def devpi_logged_in(self):
        from repo.status import check_output

        if self._args.verbose > 0:
            print('check if logged in to devpi', end=' ')
            sys.stdout.flush()
        cmd = ['devpi', 'use']
        try:
            res = check_output(cmd)
        except subprocess.CalledProcessError as e:
            print(e.output.decode('utf-8'))
            print('while running', cmd)
            sys.exit(0)
        first_line = res.split('\n', 1)[0]
        if '(not logged in)' in first_line and 'logged in as' not in first_line:
            print('devpi not logged in (check crontab?):\n  ', first_line)
            return False
        if self._args.verbose > 0:
            print('-> ok')
        return True

    def check(self):
        self.check_dist_dir()
        tox_wd = self.check_tox_dir()
        self._args.test = False
        with TmpFiles(
            self, license=True, tox=tox_wd, makefile=True, sub_packages=self.sub_packages
        ):
            if not self.environment_sane():
                print('environment is not sane')

    def push(self):
        self.check_dist_dir()
        tox_wd = self.check_tox_dir()
        with TmpFiles(
            self, license=True, tox=tox_wd, makefile=True, sub_packages=self.sub_packages
        ) as tf:
            # --from-develop gradually suppresses actions implemented in version
            # taken over by develop
            if not self.environment_sane():
                print('environment is not sane')
                return
            dd = self._args.date
            if dd in ['TODAY', None]:
                dd = date.today()
            if not self.update_readme_and_changes_files(self._version, dd):
                print('update_readme_and_changes_files FAILED')
                return
            if not self.check_commit_message_file():
                print('check_commit_message_file')
                return
            # self._version has now been set
            set_dev(False, save=True)
            if self.push_do_tox():
                return
            tf.prepare_commit()  # changes e.g. tox file
            if self.push_do_commit():
                return
            if self.push_do_tag(self._version):
                return
            self.do_push_to_ruamel_eu()
            # create tar.gz and universal bdist_wheel
            # upload
            # push to bitbucket
            # trigger rtd build

            # XXXXX
            # cmd = ['version', 'push', '--from-develop']
            # if self._args.reuse_message:
            #     cmd.append('--reuse-message')
            # if True or self._args.no_tox:
            #    cmd.append('--no-tox')
            # if self._args.test:
            #    cmd.append('--test')
            # if self._args.changestest:
            #    cmd.append('--changestest')
            # print('calling package_version', cmd)
            # os.system(' '.join(cmd))
            # print('<<<<<<<<<<<<<<<<<<<')
            # return
            # self.commit_changes()
        print('>>>>')
        # self.build_rtfd_doc()

    def do_push_to_ruamel_eu(self):
        cmd = ['hg', 'push', '--new-branch']
        try:
            print('pushing')
            show_output(cmd)
        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf-8')
            if 'there is no Mercurial repository here' in output:
                ssh_remote_mkdir()
                show_output(cmd)  # try again, don't catch errors
            else:
                print('output of hg push:\n', output)

    def rm_old_dist_dir(self):
        if self.old_dist_dir.exists():
            # manylinux1 currently creates this
            try:
                self.old_dist_dir.rmdir()
            except Exception:
                print('cannot remove "{}"'.format())

    def push_do_tox(self):
        """
        return False if ok
        """
        if not self._args.no_tox:
            cmd = ['detox', '-r']
            if self._args.e:
                cmd = ['tox', '-r']
                cmd.extend(['-e', self._args.e])
            try:
                res = show_output(cmd, show_command=True)  # NOQA
            except subprocess.CalledProcessError as e:
                print('error running tox', str(e))
                return True
        return False

    def push_do_commit(self):
        """
        return False if ok
        """
        from repo.status import status_list

        lst = status_list()
        self.version_badge()
        if lst:  # there is something to commit, normally at least __init__.py
            # commit
            if self.commit_message_file.exists():
                try:
                    show_output(['hg', 'commit', '--logfile', self.commit_message_file])
                except subprocess.CalledProcessError as e:
                    print('error committing with message file', str(e))
                    return True
                self.commit_message_file.unlink()
            else:
                os.system('hg commit')
            # make sure commit happened
            lst = status_list()
            if lst:
                print('repo not clean after commit, aborting')
                for k in lst:
                    print(' ', k)
                return True
        return False

    def push_do_tag(self, version):
        from repo.status import check_output

        str_version = '.'.join([str(x) for x in version])
        res = check_output(['hg', 'tags'])
        if self.do_tag and '\n' + str_version not in res:
            # tag if not yet there
            check_output(['hg', 'tag', str_version])
            return False
        else:
            print('already tagged')
        return True
        # push to ruamel

    def do_version(self):
        # show_output(sys.argv[1:])
        cmd = 'version ' + ' '.join(self._args.args)
        # print('cmd:', cmd)
        os.system(cmd)  # so you can edit

    def readme(self):
        """
        update date and version in Readme as necessary.
        If there is a section NEXT: followed by bullit items, take that to be the changes
        for the new version.
        """
        dd = self._args.date
        if dd in ['TODAY', None]:
            dd = date.today()
        version = [str(t) for t in self._args.version.split('.')]
        print(f'dd: {dd}')
        print(f'version: {version}')
        self.update_readme_and_changes_files(version, dd)

    def update_readme_and_changes_files(self, version, dd):
        next_text = 'NEXT:'  # has to be an empty newline before NEXT:

        def extract_next(text):
            lines = text.splitlines()
            gather = None
            version_line = None
            date_line = None
            for idx, line in enumerate(lines):
                if version_line is None and line.startswith(':version:'):
                    version_line = idx
                if date_line is None and (
                    line.startswith(':updated:') or line.startswith(':date:')
                ):
                    date_line = idx
                if line.startswith(next_text):
                    gather = []
                    continue
                if gather is None:
                    continue
                if line and line[0] != ' ':
                    break
                gather.append(line)
            if gather is None:
                return False, None, None
            return '\n'.join(gather), version_line, date_line

        def first_word_with_following_spaces(line):
            space = False
            for idx, ch in enumerate(line):
                if space and not ch.isspace():
                    return line[:idx]
                if ch.isspace():
                    space = True
            raise Exception('no space found')

        assert not self._readme.has_been_read()
        try:
            testing = self._args.test_readme_message
            print('testing', testing)
        except Exception:
            testing = False
        if testing:
            ver, testing = testing.split('|')
            self._readme.text = self._readme.text.replace(
                '\n' + ver, f'\nNEXT:\n  - {testing}\n\n{ver}'
            )
        line_with_next = self._readme.find_single_line_starting_with(
            next_text, raise_on_error=False
        )
        changes = Path('CHANGES')
        if changes.exists() and line_with_next is None:
            #  and '\n\n' + next_text not in text:
            print(f'no single {next_text} entry in README, but CHANGES exists')
            return False
        version_s = '.'.join([str(t) for t in version[:3]])
        new_version = '\n{} ({}):'.format(version_s, dd)
        # print(text[:2000])
        gather, version_line, date_line = extract_next(self._readme.text)
        if self._args.verbose > 1:
            print(
                'extracted:',
                gather,
                self._readme.lines[version_line],
                self._readme.lines[date_line],
                sep='\n',
            )
        assert gather is not None
        # update readme
        if gather:
            if self._args.verbose > 0:
                print('inserting version string', version_s)
            self._readme.text = self._readme.text.replace('\n' + next_text, new_version)
            self._readme.lines[version_line] = (
                first_word_with_following_spaces(self._readme.lines[version_line]) + version_s
            )
            self._readme.lines[date_line] = first_word_with_following_spaces(
                self._readme.lines[date_line]
            ) + str(dd)
            self._readme._text = None
            self._readme.write()
        if self._args.verbose > 1:
            print(
                'updated:',
                gather,
                self._readme.lines[version_line],
                self._readme.lines[date_line],
                sep='\n',
            )
        # update changes
        if changes.exists():
            ch_text = changes.read_text()
            version_int = [int(t) for t in version[:3]]
            changes.write_text(f'{version_int}: {dd}\n{gather}\n{ch_text}')
        return True

    docker_file_template = """
    FROM quay.io/pypa/manylinux1_x86_64:{}
    
    MAINTAINER Anthon van der Neut <a.van.der.neut@ruamel.eu>
    
    RUN echo '[global]' > /etc/pip.conf
    RUN echo 'disable-pip-version-check = true' >> /etc/pip.conf
    
    RUN echo 'cd /src' > /usr/bin/makewheel
    RUN echo 'rm -f /tmp/*.whl'                               >> /usr/bin/makewheel
    RUN echo 'for PYVER in $*; do'                            >> /usr/bin/makewheel
    RUN echo '  for PYBIN in /opt/python/cp$PYVER*/bin/; do'  >> /usr/bin/makewheel
    RUN echo '     echo "$PYBIN"'                             >> /usr/bin/makewheel
    RUN echo '     ${{PYBIN}}/pip install -Uq pip'              >> /usr/bin/makewheel
    RUN echo '     ${{PYBIN}}/pip wheel . -w /tmp'              >> /usr/bin/makewheel
    RUN echo '  done'                                         >> /usr/bin/makewheel
    RUN echo 'done'                                           >> /usr/bin/makewheel
    RUN echo ''                                               >> /usr/bin/makewheel
    RUN echo 'for whl in /tmp/*.whl; do'                      >> /usr/bin/makewheel
    RUN echo '  echo processing "$whl"'                       >> /usr/bin/makewheel
    RUN echo '  auditwheel show "$whl"'                       >> /usr/bin/makewheel
    RUN echo '  auditwheel repair "$whl" -w /src/dist/'       >> /usr/bin/makewheel
    RUN echo 'done'                                           >> /usr/bin/makewheel
    RUN chmod 755 /usr/bin/makewheel


    CMD /usr/bin/makewheel {}

    # cp27-cp27m p27-cp27mu cp34-cp34m cp35-cp35m cp36-cp36m cp37-cp37m
    """  # NOQA

    def dist(self):
        from repo.status import check_output

        many_linux = {
            '27 34 35 36': '01a75168a06f',  # 201701
            '37': 'fbf76948b80e',  # 20180724
        }
        many_linux = {'27 34 35 36 37': 'latest'}
        if self._args.rpath:
            return self.dist_rpath(self._args.rpath)
        if Path('build').exists():
            print('build directory found, run "dv clean" first')
            return
        if self._args.all:
            do_sdist = do_linux = do_macos = do_windows = True
        else:
            do_sdist = self._args.sdist
            do_linux = self._args.linux
            do_macos = self._args.macos
            do_windows = self._args.windows
        tox_wd = self.check_tox_dir()
        dist_dir = self.check_dist_dir()
        if do_linux or do_sdist:
            with TmpFiles(
                self, license=True, tox=tox_wd, makefile=True, sub_packages=self.sub_packages
            ):
                if do_sdist:
                    cmd = [sys.executable, 'setup.py', 'sdist']
                    if self._args.kw:
                        cmd.append('--dump-kw')
                    show_output(cmd)
                if do_linux:
                    for ml in sorted(many_linux):
                        self.docker_file.write_text(
                            dedent(self.docker_file_template).format(many_linux[ml], ml)
                        )
                        res = check_output(['dc', 'build'])  # NOQA
                        show_output(['dc', 'up'], verbose=True)
                    print('\033[0m')  # sometimes manylinux mixes up things wrt colors
                    self.rm_old_dist_dir()
                # self.dist_rpath('*')
        if do_macos:
            if True:
                show_output(['ssh', 'builder@macos', 'cd tmp; /usr/local/bin/hg pull -u'])
                show_output(
                    [
                        'ssh',
                        'builder@macos',
                        'rm -rf tmp/dist tmp/build; for i in 27 34 35 36 37; do source '
                        'py$i/bin/activate; cd ~/tmp; python setup.py bdist_wheel; '
                        'cd ~; deactivate; done',
                    ]
                )
            # print('dist', dist_dir)
            show_output(['scp', 'builder@macos:~/tmp/dist/*.whl', dist_dir], verbose=1)
            time.sleep(2)
            # raise NotImplementedError
        if do_windows:
            # this assumes in .hg/hgrc:
            # appveyor = ssh://hg@bitbucket.org/appveyor-ruamel/....
            d = 'cd {}; hg push appveyor --branch default --force'.format(os.getcwd())
            if self.pon.obj.get('windows_wheels'):
                # create windows wheels
                try:
                    show_output(['ssh', '-x', '-a', 'appveyor@localhost', d], verbose=1)
                except subprocess.CalledProcessError as e:
                    print('e', e)
                    pass
        versions = self.dist_versions()
        count = 0
        for version in sorted(versions, reverse=True):
            print(str(version))
            for fn in sorted(versions[version]):
                print(' ', fn.name)
            count += 1
            if count > 2:
                break
            # major, minor = get_mm(version)
            # if mm is None:
            #     mm = (major, minor)
            # elif mm[0] != major or mm[1] != minor:
            #     break
        print('+', len(versions) - count)

    def dist_versions(self):
        versions = {}
        dist_dir = self.check_dist_dir()
        pkg = self.pon.obj['full_package_name']
        for fn in dist_dir.glob(pkg + '-*'):
            version = fn.stem[len(pkg) + 1 :]
            v = xversion(version)
            versions.setdefault(v, []).append(fn)
        return versions

    def dist_rpath(self, dist, verbose=0):
        from tempfile import TemporaryDirectory

        dist = dist.replace('.', "")
        versions = self.dist_versions()
        dist_dir = self.check_dist_dir()
        version = sorted(versions, reverse=True)[0]
        for fn in sorted(versions[version]):
            if dist == '*' or dist in fn.name:
                print(' ', fn.name)
                with TemporaryDirectory(prefix='develop_') as tmpdir:
                    os.chdir(tmpdir)
                    if verbose > 0:
                        print(tmpdir)
                    sys.stdout.flush()
                    unzip = ['unzip', dist_dir / fn.name]
                    res = subprocess.check_output(unzip).decode('utf-8')
                    # print(res)
                    for so_file in Path(tmpdir).glob('*.so'):
                        readelf = ['readelf', '-d', str(so_file)]
                        res = subprocess.check_output(readelf).decode('utf-8')
                        if verbose > 0:
                            print(res)
                        sys.stdout.flush()
                        if 'RPATH' in res:
                            print('found rpath in so:', so_file)
                            chrpath = ['chrpath', '-d', str(so_file)]
                            res = subprocess.check_output(chrpath).decode('utf-8')
                            print('chrpath', res)
                            res = subprocess.check_output(readelf).decode('utf-8')
                            if verbose > 0:
                                print(res)
                            assert 'RPATH' not in res
                            # so_out = dist_dir / (fn.name + '.new')
                            so_out = so_file
                            so_out.unlink()
                            zip = ['zip', '-rq9', str(so_out), '.']
                            print('zip', zip)
                            res = subprocess.check_output(
                                zip, stderr=subprocess.STDOUT
                            ).decode('utf-8')
                            print(res)
                            sys.stdout.flush()

                    sys.stdout.flush()
        # version = sorted(versions, reverse=True)
        # print('ver', version)
        #    print(str(version))
        #    for fn in sorted(versions[version]):
        #        print(" ", fn.name)

    def build_rtfd_doc(self):
        import requests

        # rtfd is the internal number on readthedocs, inspect the [Build] button
        rtfd_id = self.pon.obj.get('rtfd')
        if rtfd_id:
            if not isinstance(rtfd_id, int):
                raise NotImplementedError
            url = 'http://readthedocs.org/build/{}/'.format(rtfd_id)
            # no login necessary
            r = requests.post(url, data={'submit': 'build'})  # NOQA

    def check_dist_dir(self):
        if not self._args.distbase:
            print('you have to set --distbase')
            sys.exit(-1)
        try:
            pkg = self.pon.obj['full_package_name']
        except AttributeError as e:
            if self.pon is None:
                print(f'no _package_data in {ununinitpy}?')
            else:
                print('Attribute error', dir(e))
            sys.exit(-1)
        dist_dir = Path(self._args.distbase) / pkg
        if not dist_dir.exists():
            dist_dir.mkdir(parents=True)
            if self.old_dist_dir.exists():
                for fn in self.old_dist_dir.glob('*'):
                    fn.copy(dist_dir / fn.name)
                    fn.unlink()
                self.old_dist_dir.rmdir()
        else:
            if self.old_dist_dir.exists():
                print('cannot have both {} and {}'.format(dist_dir, self.old_dist_dir))
                sys.exit(-1)
        return dist_dir

    def check_tox_dir(self):
        if not self._args.toxbase:
            print('you have to set --toxbase')
            sys.exit(-1)
        pkg = self.pon.obj['full_package_name']
        tox_dir = Path(self._args.toxbase) / pkg
        if self.old_tox_dir.exists():
            print('removing ', self.old_tox_dir)
            self.old_tox_dir.rmtree()
        if not tox_dir.exists():
            print('creating', tox_dir)
            tox_dir.mkdir(parents=True)
        return tox_dir

    @property
    def sub_directory_pon(self):
        # list of subdirectories that have __init__.py and obtionally pon (if not -> None)
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            pons = {}
            for path in Path('.').glob('*/' + ununinitpy):
                try:
                    with io.open(path) as fp:
                        pon = PON()
                        if pon.extract(fp, start=PKG_DATA) is None:
                            pon = None
                        else:
                            check_init_pon(path, pon)
                except IOError:
                    pon = None
                pons[str(path.parent)] = pon
            setattr(self, attr, pons)
        return getattr(self, attr)

    @property
    def sub_packages(self):
        ret_val = []
        for path in self.sub_directory_pon:
            pon = self.sub_directory_pon[path]
            if pon and pon.obj.get('nested'):
                ret_val.append(path)
        return ret_val

    # #     def test_commit_build_push(self, version, settings=None, testing=False):
    # #         """either raise an error (or don't catch), or return False to prevent
    # #         version number increment
    # #         settings are currently a subset of the __init__.py:_package_data structure
    # #         """
    ##
    # #         def confirm(x):
    # #             if sys.version_info < (3,):
    # #                 return raw_input(x)
    # #             return input(x)
    ##
    # #         def confirm_yes_no(x):
    # #             res = None
    # #             while res is None:
    # #                 resx = confirm(x)
    # #                 if resx:
    # #                     if resx in 'yY':
    # #                         res = True
    # #                     if resx in 'nN':
    # #                         res = False
    # #             return res
    ##
    # #         def distribution_files(name, version, windows_wheel=False, any_wheel=False,
    # #                                many_wheel=False):
    # #             from glob import glob
    # #             n = self.fpn if name is None else name
    # #             dn = os.environ['PYDISTBASE'] + '/' + n
    # #             v = u'.'.join([str(x) for x in version])
    # #             tgv = u'{}/{}-{}.tar.gz'.format(dn, n, v)
    # #             tbv = u'{}/{}-{}.tar.bz2'.format(dn, n, v)
    # #             txv = u'{}/{}-{}.tar.bz2'.format(dn, n, v)
    # #             av = u'{}/{}-{}-*-any.whl'.format(dn, n, v)
    # #             wv = u'{}/{}-{}-*-win*.whl'.format(dn, n, v)
    # #             mv = u'{}/{}-{}-*-manylinux*.whl'.format(dn, n, v)
    # #             ok = True
    # #             for tv in [tbv, tgv, txv]:  # most likely order
    # #                 ret_val = glob(tv)
    # #                 if len(ret_val) != 1:
    # #                     # print('matching ', repr(tv), ret_val)
    # #                     pass
    # #                 else:
    # #                     break
    # #             else:
    # #                 ok = False
    # #             if any_wheel:
    # #                 ret_val.extend(glob(av))
    # #                 if len(ret_val) <= 1:
    # #                     print('matching ', repr(wv), ret_val)
    # #                     ok = False
    # #             if windows_wheel:
    # #                 ret_val.extend(glob(wv))
    # #                 if len(ret_val) <= 1:
    # #                     print('matching ', repr(wv), ret_val)
    # #                     ok = False
    # #             if many_wheel:
    # #                 ret_val.extend(glob(mv))
    # #                 if len(ret_val) <= 1:
    # #                     print('matching ', repr(mv), ret_val)
    # #                     ok = False
    # #             if not ok:
    # #                 print('distribution_files not ok')
    # #                 sys.exit(0)
    # #             return ret_val
    ##
    # #         docker_compose_file = Path('docker-compose.yml')
    # #         version = [x for x in version if x != u'dev']  # remove dev
    # #         if settings is None:
    # #             settings = {}
    # #         from repo.status import check_output, status_list
    # #         # run tox (optional incrementally?)
    # #         if self.do_tox:
    # #             cmd = ['tox']
    # #             # this was in order not to rebuild virtualenv if e.g. only flake8 failed
    # #             # if True or not getattr(self._args, 'reuse_message', False):
    # #             cmd.append('-r')
    # #             print('running', ' '.join(cmd))
    # #             try:
    # #                 res = show_output(cmd)
    # #             except subprocess.CalledProcessError as e:
    # #                 print('error running tox', e.message)
    # #                 return
    # #         lst = status_list()
    # #         if lst:  # there is something to commit, normally at least __init__.py
    # #             # commit
    # #             if self.commit_message_file.exists():
    # #                 try:
    # #                     show_output(['hg', 'commit', '--logfile',
    # #                                 self.commit_message_file])
    # #                 except subprocess.CalledProcessError as e:
    # #                     print('error committing with message file', e.message)
    # #                     return
    # #                 self.commit_message_file.unlink()
    # #             else:
    # #                 os.system('hg commit')
    # #             # make sure commit happened
    # #             lst = status_list()
    # #             if lst:
    # #                 print('repo not clean after commit, aborting')
    # #                 for k in lst:
    # #                     print(' ', k)
    # #                 return False
    # #         # XXXXX
    # #         str_version = u'.'.join([str(x) for x in version])
    # #         res = check_output(['hg', 'tags'])
    # #         if self.do_tag and u'\n' + str_version not in res:
    # #             # tag if not yet there
    # #             check_output(['hg', 'tag', str_version])
    # #         else:
    # #             print('already tagged')
    # #         # push to ruamel
    # #         try:
    # #             print('pushing')
    # #             check_output(['hg', 'push', '--new-branch'])
    # #         except subprocess.CalledProcessError as e:
    # #             if 'there is no Mercurial repository here' in e.output:
    # #                 ssh_remote_mkdir()
    # #                 check_output(['hg', 'push'])  # try again, don't catch errors
    # #             else:
    # #                 print('output of hg push:\n', e.output)
    # #         # create dist
    # #         show_output(['python', 'setup.py', 'sdist'], verbose=1)
    # #         if settings.get('universal'):
    # #             show_output(['python', 'setup.py', 'bdist_wheel'], verbose=1)
    # #             print('\nself nested', self.nested)
    # #             if self.nested:
    # #                 dist_dir = Path(os.environ['PYDISTBASE']) / self.fpn
    # #                 print('\nnested1', dist_dir)
    # #                 full_name = list(dist_dir.glob('{}-{}*.whl'.format(self.fpn,
    # #                                        str_version)))
    # #                 print('full_name', full_name)
    # #                 if len(full_name) != 1:
    # #                     print('should find one element')
    # #                     sys.exit(-1)
    # #                 full_name = full_name[0]
    # #                 with InMemoryZipFile(full_name) as imz:
    # #                     imz.delete_from_zip_file(self.fpn + '.*.pth')
    # #                 # self.press_enter_to_continue('fix wheel (remove nspkg.pth) \
    # #                           and press Enter')
    # #         if docker_compose_file.exists():
    # #             show_output(['/opt/util/docker-compose/bin/dcw', 'up'], verbose=1)
    # #         # track size changes, compared to previous run
    # #         # upload
    # #         if self.do_upload:
    # #             cmd = ['twine', 'upload']
    # #             cmd.extend(distribution_files(None, version,
    # #                                           windows_wheel=False,
    # #                                           any_wheel=settings.get('universal'),
    # #                                           many_wheel=docker_compose_file.exists(),
    # #                                           ))
    # #             show_output(cmd, verbose=1, stderr=subprocess.PIPE)
    # #         # 20170624 trying to upload a tar.bz2:
    # #         # Uploading ruamel.yaml-0.15.11.tar.bz2
    # #         # error HTTPError: 400 Client Error: Invalid file extension.
    # #         #    for url: https://upload.pypi.org/legacy/
    ##
    # #         # push to devpi? or to pypi using devpi
    # #         # "devpi upload" cleans out the dist directory and is therefore useless
    # #         # check_output(['devpi', 'upload', '--from-dir', 'dist', '--only-latest'])
    # #         # potentially push to other servers running devpi
    # #         # push to pypi, using twine
    # #         if False:
    # #             pass
    # #         # push to bitbucket
    # #         try:
    # #             show_output(['ssh', '-x', '-a', 'ruamel@localhost',
    # #                     'cd {}; hg push bitbucket --branch default'.format(os.getcwd())],
    # #                         verbose=1)
    # #             prj = settings.get('read_the_docs')
    # #             if prj is not None:
    # #                 trigger_rtd_build(prj)
    # #         except subprocess.CalledProcessError as e:
    # #             pass
    # #         return True

    def walk(self):
        tox_dir = '.tox'
        hg_dir = '.hg'
        skip_dirs = [
            tox_dir,
            hg_dir,
            '.cache',
            '.ruamel',
            '.repo',
            '__pycache__',
            '.pytest_cache',
        ]
        if self._args.check_init:
            skip_dirs.extend(['_test', 'build', 'dist'])
        # for x in Path('.').glob('**/__init__.py'):
        #    print(x)
        count = 0
        for root, directories, files in os.walk('.'):
            dirs_no_recurse = []
            # print('root', root)
            if root == './ruamel/util/new/templates':
                continue
            for d in directories:
                if d in skip_dirs or d.endswith('.egg-info'):
                    dirs_no_recurse.append(d)
            for d in dirs_no_recurse:
                if d in directories:
                    directories.remove(d)
            if self._args.check_init and '__init__.py' in files:
                if self.walk_check_init(Path(root)):
                    count += 1
            elif self._args.insert_pre_black and '__init__.py' in files:
                if self.insert_pre_black(Path(root)):
                    count += 1
            elif self._args.check_hgignore and dot_hgignore in files:
                if self.walk_check_hgignore(Path(root)):
                    count += 1
            # print(root)
        print('count:', count)

    def walk_check_hgignore(self, root):
        hgi = HgIgnore(root / dot_hgignore)
        print('hgignore file', str(hgi._file_name).replace(os.getcwd(), '.'))
        # print('############# global hgignore:')
        glob_hgi = GlobalHgIgnore()
        # print(glob_hgi.text)
        # print('############# .hgignore:')
        # print(hgi.text)
        # print('nr. of lines:', len(hgi.lines))
        res = hgi.remove_lines_already_in_global(glob_hgi, verbose=1)
        if res == 2:
            hgi._file_name.unlink()
        elif res == 1:
            # print(hgi.text)
            hgi._file_name.write_text(hgi.text)
            pass
        # print(hgi.text)
        # print('nr. of lines:', len(hgi.lines))
        return 1

    @staticmethod
    def display_name(size, dts, root):
        print('{:-6} {:%Y-%m-%d} {}'.format(size, dts, root))

    def has_package_data(self, init_py):
        st = init_py.stat()
        size = st.st_size
        if size == 0:
            return False
        dts = datetime.datetime.fromtimestamp(st.st_mtime)
        package_data = False
        for line in init_py.read_text().splitlines():
            if 'JSON' in line and not package_data:
                self.display_name(size, dts, init_py.parent)
                print('old JSON package information found, use packageversion to convert')
                sys.exit(1)
            if line.startswith('_package_data'):
                package_data = True
        if package_data:
            return True
        return False

    def walk_check_init(self, root):
        init_py = root / '__init__.py'
        if not self.has_package_data(init_py):
            return False
        pon = PON()
        with io.open(str(init_py)) as fp:
            pon.extract(fp, start=PKG_DATA)
            # check_init_pon(ununinitpy, pon)
        new_vers = pon.obj.get('__version__')
        convert_vers = '_convert_version' in init_py.read_text()
        if new_vers is None:
            bup = init_py.with_suffix('.py.orig2')
            if not bup.exists():
                init_py.copy(bup)
            self.add_string_version(init_py)
            return True
        if new_vers is None and convert_vers:
            print('check versioning', root)
        return True

    def add_string_version(self, path):
        vinf = '    version_info=('
        text = path.read_text()
        assert '    __version__=' not in text
        lines = text.splitlines()
        new_lines = []
        skipping = False
        for _idx, line in enumerate(lines):
            if line.startswith(vinf):
                new_lines.append(line)
                v = [x.strip() for x in line.split('(')[1].split(')')[0].split(',')]
                # text = "    __version__='{}',".format('.'.join(v)
                # text = '\n'.join(
                #    lines[:idx+1] +
                #    ["    __version__='{}',".format('.'.join(v))] +
                #    lines[idx:]
                # )
                new_lines.append("    __version__='{}',".format('.'.join(v)))
                continue
            if not skipping and '_convert_version' in line:
                skipping = True
                continue
            if line.startswith('del _convert_version'):
                skipping = False
                new_lines.append("version_info = _package_data['version_info']")
                new_lines.append("__version__ = _package_data['__version__']")
                continue
            if skipping:
                continue
            new_lines.append(line)
        text = '\n'.join(new_lines)
        # print(text)
        path.write_text('\n'.join(new_lines))

    def insert_pre_black(self, root):
        import shutil

        print(root)
        init_py = root / '__init__.py'
        if not self.has_package_data(init_py):
            return False
        pon = PON()
        try:
            with io.open(str(init_py)) as fp:
                pon.extract(fp, start=PKG_DATA)
            if not pon.obj.get('black') and not pon.obj.get('pre_black'):
                if True:
                    print('root', root)
                    pon.obj['pre_black'] = True
                    shutil.copy(str(init_py), str(init_py) + '.orig')
                    pon.update(str(init_py), start=PKG_DATA)
                    sys.exit(1)
                return True
        except Exception as e:
            print('root:', root)
            raise

    def black(self):
        import glob
        from itertools import chain

        _black = self.pon.obj.get('black', [])
        if not isinstance(_black, list):
            _black = _black.strip().split()
        print('self._args.files', self._args.files)
        args = list(
            chain.from_iterable(
                [
                    glob.glob(x)
                    for x in (self._args.files if self._args.files else ['*.py', '_test/*.py'])
                ]
            )
        )
        print('args', args)
        diff = ['--diff'] if self._args.diff else []
        cmd = ['black'] + _black + diff + args
        print('cmd:', cmd)
        show_output(cmd)


###################################################


def x1version(version):
    from cmp_version import VersionString

    class MyVS(VersionString):
        def __hash__(self):
            return hash(str(self))

    dv = version.split('.tar', 1)[0]
    dv = dv.split('-cp', 1)[0]
    dv = dv.split('-py', 1)[0]
    dv = dv.replace('.dev0', '.a0')

    v = MyVS(dv)
    if 'xxdev' in version:
        print(v, repr(v))
    return v
    return
    from .version import Version

    version = version.replace('.dev0', '.a')
    v = Version(version)
    if 'alph' in version:
        print(v, repr(v))
    return v
    ret = []
    for n in version.replace('-', '.', 1).split('.'):
        try:
            ret.append('{:03d}'.format(int(n)))
        except ValueError:
            ret.append(n)
    return tuple(ret)


def xversion(version):
    # use verlib?
    # pip has semantic versioning as well, verlib does
    from pip._vendor.distlib.version import NormalizedVersion

    dv = version.split('.tar', 1)[0]
    dv = dv.split('-cp', 1)[0]
    dv = dv.split('-py', 1)[0]

    return NormalizedVersion(dv)
    # print(dir(v))
    # print(v._parts)


def check_init_pon(path, pon):
    irs = pon.obj.get('install_requires', [])
    if isinstance(irs, dict):
        if 'any' in irs:
            if len(irs) == 1:
                pon.obj['install_requires'] = irs['any']
                pon.update(path, start=PKG_DATA)
            else:
                raise NotImplementedError('install_requires should be a list')
    ep = pon.obj.get('entry_points')
    if ep:
        for ir in irs:
            if ir.startswith('ruamel.std.argparse'):
                try:
                    v = ir.split('>=')[1]
                except Exception:
                    try:
                        v = ir.split('>')[1]
                    except Exception:
                        v = '0.1'
                v = tuple(map(int, v.split('.')))
                min_ver = (0, 8)
                if not v >= min_ver:
                    print(
                        'need at least version {} < {} in {} for ruamel.std.argparse'.format(
                            str(v), str(min_ver), path
                        )
                    )
                    sys.exit(1)
    # print('ep', ep)
    #        v = list(p.obj['version_info'])
    #        v[1] += 1 # update minor version
    #        v[2] = 0 # set micro version
    #        p.obj['version_info'] = tuple(v)
    #        p.update(file_name, start=s, typ=t)


def ssh_remote_mkdir():
    from repo.status import check_output
    from configobj import ConfigObj

    conf = ConfigObj(open('.hg/hgrc'))
    path = conf['paths']['default-push']
    ssh, rest = path.split('//', 1)
    user_host, path = rest.split('/', 1)

    cmd = ['ssh', user_host, 'mkdir -p {path} ; hg init {path}'.format(path=path)]
    res = check_output(cmd)
    print(res)


# def get_mm(v):
#     return v._parts[1][0], v._parts[1][1]
