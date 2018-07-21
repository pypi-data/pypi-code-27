'''
loader

Discover and load performance test modules.
'''
import os
import re
import imp
import sys
import inspect
import traceback
from colorama import Fore, Back

from .suite import Suite

V_QUIET = 0
V_NORMAL = 1
V_LOUD = 2
V_DEBUG = 3
VERBOSITY = V_NORMAL


def _traceback(s):
    lines = s.splitlines()
    lines = ['    ' + lines[0]] + lines[3:]
    return '\n    '.join(lines)


def _compile_re(s):
    if isinstance(s, str):
        return re.compile(s)
    return s


def _vprint(msg, verbosity, color=None, back=None):
    if verbosity >= VERBOSITY:
        if color:
            color = getattr(Fore, color.upper())
        else:
            color = Fore.RESET
        if back:
            back = getattr(Back, back.upper())
        else:
            back = Back.RESET
        print(color + back + msg + Fore.RESET + Back.RESET)


class Module:

    def __init__(self, module):
        if isinstance(module, str):
            module = self.load_module(module)
        self.name = module.__name__
        self.module = module
        self.classes = []
        self.functions = []

    def load_module(self, path):
        if not os.path.exists(path):
            raise ValueError('{} module does not exist'.format(path))
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)
        file, mod_path, details = imp.find_module(name, path=[dirname])
        return imp.load_module(name, file, mod_path, details)

    def discover(self, func_pattern):
        _vprint('Discovering tests in module {}'.format(self.name), V_NORMAL,
                color='blue')
        re_func = _compile_re(func_pattern)
        members = inspect.getmembers(self.module)
        self.classes = [
            (name, cls)
            for name, cls in members
            if inspect.isclass(cls) and issubclass(cls, Suite) and
            cls is not Suite
        ]
        self.functions = [
            (name, func)
            for name, func in members
            if re_func.match(name) and inspect.isfunction(func)
        ]
        _vprint('{}: found {} functions and {} Suites'.format(
            self.name, len(self.functions), len(self.classes),
        ), V_NORMAL, color='blue')

    def run(self):
        _vprint('Running {}'.format(self.name), V_NORMAL, color='blue')
        errors = {}
        fails = {}
        for name, func in self.functions:
            errors[name] = None
            fails[name] = None
            try:
                func()
            except AssertionError as e:
                sys.stdout.write('F')
                fails[name] = str(e)
            except Exception as e:
                sys.stdout.write('E')
                errors[name] = traceback.format_exc()
                continue
            else:
                sys.stdout.write('.')

        suites = []
        for name, cls in self.classes:
            suite = cls()
            suites.append(suite)
            for result in suite.run():
                if result.result == result.PASS:
                    sys.stdout.write('.')
                elif result.result == result.FAIL:
                    sys.stdout.write('F')
                elif result.result == result.ERROR:
                    sys.stdout.write('E')

        print('\n')

        for name in sorted(fails.keys()):
            if fails[name] is not None:
                _vprint('{}::{} -- {}'.format(self.name, name, fails[name]),
                        V_NORMAL, color='yellow')

        for suite in suites:
            for result in suite.results:
                if result.result == result.FAIL:
                    _vprint('{}::{}.{} -- {}'.format(
                        self.name, suite.__class__.__name__, result.name,
                        result.message or 'FAIL'
                    ), V_NORMAL, color='yellow')

        for name in sorted(fails.keys()):
            if errors[name] is not None:
                _vprint(
                    '\n{}::{}'.format(self.name, name),
                    V_NORMAL, color='magenta',
                )
                _vprint(_traceback(errors[name]) + '\n', V_NORMAL,
                        color='red')

        for suite in suites:
            for result in suite.results:
                if result.result == result.ERROR:
                    _vprint(
                        '\n{}::{}.{}'.format(
                            self.name, suite.__class__.__name__, result.name,
                        ),
                        V_NORMAL, color='magenta',
                    )
                    _vprint(_traceback(result.tb) + '\n', V_NORMAL,
                            color='red')


class Loader:

    def __init__(self, root='.', pattern=r'^perftest_.*\.py$',
                 func_pattern=r'^test_'):
        self.tests = {}
        self.pattern = _compile_re(pattern)
        self.modules = []
        module_paths = []
        if os.path.isfile(root):
            module_paths = [root]
        elif os.path.isdir(root):
            module_paths = self.discover_modules(root)
        else:
            raise ValueError('root must be a filepath or directory, got '
                             'instead: {}'.format(root))
        for module in module_paths:
            mod = Module(module)
            mod.discover(func_pattern)
            self.modules.append(mod)

    def discover_modules(self, root):
        for dirname, _, filenames in os.walk(root):
            for filename in filenames:
                if not self.pattern.match(filename):
                    continue
                path = os.path.join(dirname, filename)
                _vprint('Found module path: {}'.format(path), V_NORMAL,
                        color='blue')
                yield path

    def run(self):
        for module in self.modules:
            module.run()
