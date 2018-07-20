"""Helper functions for displaying the content of the config system"""

import inspect
import itertools
import pprint
import sys
from typing import Iterable, Tuple, List

from mara_config import get_contributed_functionality

from . import get_declared_config, get_overwritten_config

_UNSET = object()


class ConfigFunction():
    """A object which holds information about a config function"""

    def __init__(self, name):
        self.config_name = name
        self.set_func = None
        self.declared_func = None
        self.include_parent = False
        self.needs_set = False
        self.__initialized = False

    def _build_data(self):
        if self.__initialized:
            return
        sig = inspect.signature(self._value_func)
        self._signature = sig
        self.argument_length = len(sig.parameters)
        self.func_name = self._value_func.__name__
        self.module_name = self._value_func.__module__
        self.error = None
        self.value = _UNSET

        def _set_generic_exception_error(e):
            self.error = f"ERROR while calling Function {self.func_desc}: {e.__class__.__name__}: {str(e)}"

        def _set_needs_to_be_configured_error():
            self.error = f"ERROR: Config '{self.config_name}' needs to be configured before usage."

        def _set_function_as_value():
            # In the end pprint will call repr(self) on it and that does the right thing here
            self.value = self

        # At this point we can aussume that we do not need to call _build_data again and indeed
        # by using self.func_desc we would if this is not set
        self.__initialized = True

        if self.needs_set and not self.set_func:
            # this happens when we use the decoarator but the real functions returns something
            _set_needs_to_be_configured_error()
        else:
            try:
                self.value = self._value_func()
            except NotImplementedError as e:
                if not self.set_func:
                    # not overwritten, but seems to be a function which
                    # needs to be overwritten, so treat it accordingly
                    self.needs_set = True
                    _set_needs_to_be_configured_error()
                else:
                    # overwritten, but still failing -> error
                    _set_generic_exception_error(e)
            except TypeError as e:
                if self.argument_length != 0:
                    # expected because of missing arguments, so no error
                    _set_function_as_value()
                else:
                    _set_generic_exception_error(e)
            except RuntimeError as e:
                if 'application context' in str(e):
                    # needs a flask context, so expected and no error...
                    _set_function_as_value()
                else:
                    _set_generic_exception_error(e)
            except Exception as e:
                _set_generic_exception_error(e)

    @property
    def _value_func(self):
        return self.set_func or self.declared_func

    @property
    def validates(self):
        self._build_data()
        return self.error is None

    @property
    def doc(self):
        """Documentations of the set function or the declared function (first wins)"""
        doc = ''
        if self.set_func:
            doc = self.set_func.__doc__
        if not doc and self.declared_func:
            doc = self.declared_func.__doc__
        return doc or ''

    @property
    def func_desc(self):
        """String representation of the configured function"""
        self._build_data()
        args = []
        for i in self._signature.parameters.values():
            args.append(i.name)
        arg_spec = ', '.join(args)
        return f'{self.module_name}.{self.func_name}({arg_spec})'

    @property
    def state_desc(self):
        """Information about the state of the config functions

        State includes (in this order):
        * S: Whether this config was set
        * D: Whether this config was declared (might be off if the declaration is not in a module included
             in a MARA_CONFIG_MODULE)
        * I: Whether the declared function is passed in to the setfunction
        * N: Whether the declared function needs to be set

        """
        self._build_data()
        state = (('S' if self.set_func else '-') +
                 ('D' if self.declared_func else '-') +
                 ('I' if self.include_parent else '-') +
                 ('N' if self.needs_set else '-'))
        return state

    @property
    def value_desc(self):
        """Representation of the value of the config function"""
        self._build_data()
        if not self.error:
            return pprint.pformat(self.value)
        else:
            return self.error

    def __repr__(self):
        return f"<function {self.func_desc}>"


class ConfigModule():
    """All config functions in a module"""

    def __init__(self, module, contributed):
        self.module = module
        self.name = module.__name__
        self.doc = module.__doc__
        self.contributed = contributed
        self.config_functions = {}

    def get_or_build_function(self, name):
        """Creates or returns the already included ConfigFunction for the name"""
        if name in self.config_functions:
            return self.config_functions['name']
        cf = ConfigFunction(name)
        self.config_functions[name] = cf
        return cf

    def items(self) -> Iterable[Tuple[str, ConfigFunction]]:
        return sorted(self.config_functions.items())


class ConfigForDisplay():
    """The config as a iterable data structure for displaying"""

    def __init__(self):
        self._contributed = {}
        self._uncontributed = {}

    def add_module(self, module: ConfigModule):
        """Adds a ConfigModule"""
        if module.contributed:
            self._contributed[module.name] = module
        else:
            self._uncontributed[module.name] = module

    def get_or_build_module(self, module_name):
        """Creates or returns the already included ConfigModule for the name"""
        if module_name in self._contributed:
            return self._contributed[module_name]
        if module_name in self._uncontributed:
            return self._uncontributed[module_name]
        cm = ConfigModule(sys.modules[module_name], False)
        self.add_module(cm)
        return cm

    def get_function(self, key):
        """Returns the function for key, if it is included in any module"""
        for _, module in self.items():
            if key in module.config_functions:
                return module.config_functions[key]

    def items(self) -> Iterable[Tuple[str, ConfigModule]]:
        return itertools.chain(sorted(self._contributed.items()), sorted(self._uncontributed.items()))


def get_config_for_display() -> ConfigForDisplay:
    """Returns the whole known config

    The ConfigForDisplay contains ConfigModules which contain
    ConfigFunctions.

    Will load all config modules contributed via `MARA_CONFIG_MODULES`.
    """

    config = ConfigForDisplay()

    for module, config_module in get_contributed_functionality('MARA_CONFIG_MODULES'):
        config.add_module(ConfigModule(config_module, contributed=True))

    for key, (func, needs_set) in get_declared_config():
        cm = config.get_or_build_module(func.__module__)
        cf = cm.get_or_build_function(key)
        cf.declared_func = func
        cf.needs_set = needs_set
    for key, v in get_overwritten_config():
        func, include_parent = v
        cf = config.get_function(key)
        if not cf:
            cm = config.get_or_build_module(func.__module__)
            cf = cm.get_or_build_function(key)
        cf.set_func = func
        cf.include_parent = include_parent
    return config


def print_config():
    config = get_config_for_display()
    # Get to longest key length
    max_len = 0
    for _, config_module in config.items():
        for k, _ in config_module.items():
            max_len = max(len(k), max_len)

    format_str = f'%-{max_len}s [%s] -> %-{20-max_len}s'
    print('\nConfig:\n-------\n')

    for module_name, config_module in config.items():
        # print(f'# Module: {module_name}')
        for conf_name, conf_func in config_module.items():
            print(format_str % (conf_name, conf_func.state_desc, str(conf_func.value_desc)))

    print('\nS: config is set, D: @declare_config was called, I: config value includes parent, ' +
          'N: config value needs to be set\n')


def validate_config()  -> List[str]:
    """Validates all config items if needed entries are set

    Returns:
        is_good: bool, whether or not the current config validates
        validation_errors: list of strings of error messages per config item
    """
    config = get_config_for_display()
    validation_errors = []
    for module_name, config_module in config.items():
        # print(f'# Module: {module_name}')
        for conf_name, conf_func in config_module.items():
            if not conf_func.validates:
                if conf_func.needs_set and not conf_func.set_func:
                    validation_errors.append(f"UNSET: {conf_name}")
                else:
                    validation_errors.append(f"ERROR: {conf_name} ({conf_func.error})")
    return validation_errors


def generate_local_setup() -> List[str]:
    """Generates a local_setup.py content for all config items which need to be set

    Returns:
        code: list of strings with the suggested code
    """
    import inspect
    import re
    at_declare = re.compile(r'^@declare_config.*$', flags=re.MULTILINE)
    config = get_config_for_display()
    code = []
    code.append('# generated, please adjust!\n')
    code.append('from mara_config import set_config\n')

    for module_name, config_module in config.items():
        for conf_name, conf_func in config_module.items():
            if conf_func.needs_set and not conf_func.set_func:
                code.append(f"\n@set_config('{conf_func.config_name}')")
                declared_body = inspect.getsource(conf_func.declared_func)
                for line in declared_body.splitlines():
                    # remove the @delcare(...) line completely
                    if not at_declare.match(line):
                        code.append(line)
    return code
