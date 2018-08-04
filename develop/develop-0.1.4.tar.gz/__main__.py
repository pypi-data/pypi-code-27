# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import sys
import os  # NOQA

from ruamel.std.argparse import (
    ProgramBase,
    option,
    CountAction,
    SmartFormatter,
    sub_parser,
    version,
    DateAction,
    SUPPRESS,
    store_true,
)
from ruamel.appconfig import AppConfig
from . import __version__
from .develop import Develop


def to_stdout(*args):
    sys.stdout.write(' '.join(args))


alt_names = dict(
    dvm='make',
    dvt='tox',
    dvpt='pytest',
    dv8='flask8',
    dvr='repo',  # hg/git
    dvv='version',  # hg/git
)


class DevelopCmd(ProgramBase):
    def __init__(self):
        cmd = sys.argv[0].rsplit('/', 1)[-1]
        alt = alt_names.get(cmd)
        if alt:
            sys.argv.insert(1, alt)
        super(DevelopCmd, self).__init__(
            formatter_class=SmartFormatter,
            # aliases=True,
            # usage="""""",
        )

    # you can put these on __init__, but subclassing DevelopCmd
    # will cause that to break
    @option(
        '--verbose',
        '-v',
        help='increase verbosity level',
        action=CountAction,
        const=1,
        nargs=0,
        default=0,
        global_option=True,
    )
    @option(
        '--distbase', help='base directory for all distribution files (default: %(default)s)'
    )
    @option('--toxbase', help='base directory for all .tox directories (default: %(default)s)')
    @option('--keep', help='keep temporary files', action=store_true, global_option=True)
    @option(
        '--date',
        action=DateAction,
        default='TODAY',
        metavar='DATE',
        help='update date README.rst to %(metavar)s (default: %(default)s)',
    )
    @version('version: ' + __version__)
    def _pb_init(self):
        # special name for which attribs are included in help
        pass

    def run(self):
        if self._args.distbase:
            # where the distribution files live
            os.environ['PYDISTBASE'] = self._args.distbase
        self.develop = Develop(self._args, self._config)
        if hasattr(self._args, 'func'):  # not there if subparser selected
            return self._args.func()
        self._parse_args(['--help'])  # replace if you use not subparsers

    def parse_args(self):
        self._config = AppConfig(
            'develop',
            filename=AppConfig.check,
            parser=self._parser,  # sets --config option
            warning=to_stdout,
            add_save=True,  # add a --save-defaults (to config) option
        )
        # self._config._file_name can be handed to objects that need
        # to get other information from the configuration directory
        self._config.set_defaults()
        self._parse_args(
            # default_sub_parser="",
        )

    @sub_parser(help='clean up development directory')
    @option('args', nargs='*')
    def clean(self):
        self.redirect()

    @sub_parser(help='execute dist related commands')
    @option('--all', action=store_true, help='build sdist wheels for all platforms')
    @option('-s', '--sdist', '--src', action=store_true, help='build sdist')
    @option('--linux', action=store_true, help='build linux wheels using manylinux')
    @option('--macos', action=store_true, help='build macOS wheels')
    @option('--windows', action=store_true, help='build windows wheels on appveyor')
    @option('--rpath', help="remove rpath from .so in manylinux build ('*' for all)")
    @option('--kw', action=store_true, help='show keywords as calculated by setup.py')
    def dist(self):
        self.redirect()

    @sub_parser(help='invoke make (with args), writes .Makefile.tmp')
    @option('args', nargs='*')
    def make(self):
        self.redirect()

    @sub_parser(help='invoke mypy --strict')
    # @option('args', nargs='*')
    def mypy(self):
        self.redirect()

    @sub_parser(help='create and push a new release')
    @option('--test', action=store_true, help="test only don't push to PyPI")
    @option('--changestest', action=store_true, help='test update of CHANGES')
    @option(
        '--reuse-message', '--re-use-message', action=store_true, help='reuse commit message'
    )
    @option('--commit-message', help='use commit message (no interaction)')
    @option('--no-tox', action=store_true, help="don't run tox -r")
    @option('--test-readme-message', help=SUPPRESS)
    @option('-e', help=SUPPRESS)
    def push(self):
        self.redirect()

    @sub_parser(help='execute Read the Docs related commands')
    @option('--build', action=store_true, help='trigger build')
    def rtfd(self):
        self.redirect()

    @sub_parser(help='execute Read the Docs related commands')
    @option('--version', metavar='X.Y.Z', help='update version in README.rst to %(metavar)s')
    @option(
        '--date',
        action=DateAction,
        default='TODAY',
        metavar='DATE',
        help='update date README.rst to %(metavar)s (default: %(default)s)',
    )
    def readme(self):
        self.redirect()

    @sub_parser(help='invoke tox (with args)')
    @option('-e', metavar='TARGETS', help='only test comma separated %(metavar)s')
    @option(
        '-r',
        action=store_true,
        help='force recreation of virtual environments by removign them first',
    )
    @option('args', nargs='*')
    def tox(self):
        self.redirect()

    @sub_parser(help='execute version related commands')
    @option('--badge', action=store_true, help='write version in PyPI badge')
    @option('args', nargs='*')
    def version(self):
        self.redirect()

    @sub_parser(help='check sanity of the package (also done on push)')
    def check(self):
        self.redirect()

    @sub_parser(help='run black on the arguments (on .py and _test/*.py if no arguments)')
    @option('--diff', action=store_true)
    @option('files', nargs='*')
    def black(self):
        self.redirect()

    @sub_parser(help='walk the development tree recursively and execute actions')
    @option('--check-init', action=store_true, help='check __init__.py files')
    @option(
        '--insert-pre-black',
        action=store_true,
        help='insert pre-black entry in __init__.py files',
    )
    @option(
        '--check-hgignore',
        action=store_true,
        help='remove entries in .hgignore files that are in global ignore file, '
        'delete when emtpy',
    )
    def walk(self):
        self.redirect()

    def redirect(self, *args, **kw):
        """
        redirect to a method on self.develop, with the same name as the
        method name of calling method
        """
        getattr(self.develop, sys._getframe(1).f_code.co_name)(*args, **kw)


def main():
    n = DevelopCmd()
    n.parse_args()
    sys.exit(n.run())


if __name__ == '__main__':
    main()
