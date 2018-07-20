import logging

import pytest
import sys
from mara_config import declare_config, set_config
from mara_config.config_system import add_config_from_environment, _reset_config
from mara_config.config_system.config_display import get_config_for_display


# this dance with orig_something and so on is needed so 'something' is actually decorated by the fixture
# and the config can be cleaned up
def something(argument: str = None) -> str:
    "Test API function"
    return "x"


orig_something = something


def without_args() -> str:
    "Test without arguments"
    return "x"


orig_without_args = without_args


@pytest.fixture()
def setup_config():
    """Setup a clean config and insert a single API"""
    _reset_config()
    logging.root.setLevel(logging.DEBUG)
    global something
    global without_args
    something = declare_config()(orig_something)
    without_args = declare_config()(orig_without_args)
    yield setup_config
    _reset_config()


# use it in every tests in this file
pytestmark = pytest.mark.usefixtures("setup_config")


def test_config_decorator():
    @declare_config()
    def _tester(argument: str = None) -> str:
        return "x"

    # unreplaced
    assert 'x' == _tester()
    assert 'x' == _tester("ABC")


def test_replace_decorator_without_function_pointer():
    # In downstream package which want's to overwrite the API
    @set_config('mara_config.tests.test_config.something')
    def replacement_for_something(argument: str = None) -> str:
        return argument or 'y'

    assert 'y' == something()
    assert 'ABC' == something("ABC")


def test_replace_decorator_with_include_orig_function():
    # In downstream package which want's to overwrite the API
    @set_config('mara_config.tests.test_config.something', include_original_function=True)
    def replacement_for_something(argument: str = None, original_function=None) -> str:
        if original_function:
            val = original_function()
        else:
            val = ''
        return val + (argument or 'y')

    assert 'xy' == something()
    assert 'xABC' == something("ABC")


# this can only be wrapped once!
def _to_be_wraped_once():
    return 'x'

def test_wraps():

    before = _to_be_wraped_once
    assert 'x' == _to_be_wraped_once()

    from mara_config.config_system import wrap

    @wrap(_to_be_wraped_once)
    def replacement(original_function) -> str:
        str(original_function)
        val = original_function()
        return val + 'y'
    after = _to_be_wraped_once
    assert before != after
    assert 'xy' == _to_be_wraped_once()

    # check that it shows up correctly in the config views
    config = get_config_for_display()
    for module_name, config_module in config.items():
        # print(f'# Module: {module_name}')
        for conf_name, conf_func in config_module.items():
            if '_to_be_wraped_once' in conf_name:
                assert conf_func.include_parent
                assert not conf_func.needs_set
                assert conf_func.set_func
                assert conf_func.declared_func


# this can only be patched once!
def _to_be_patched_once():
    return 'x'

def test_patch():

    assert 'x' == _to_be_patched_once()

    from mara_config.config_system import patch

    @patch(_to_be_patched_once)
    def replacement() -> str:
        return 'y'

    assert 'y' == _to_be_patched_once()
    # check that it shows up correctly in the config views
    config = get_config_for_display()
    for module_name, config_module in config.items():
        # print(f'# Module: {module_name}')
        for conf_name, conf_func in config_module.items():
            if '_to_be_patched_once' in conf_name:
                assert not conf_func.include_parent
                assert not conf_func.needs_set
                assert conf_func.set_func
                assert conf_func.declared_func


def test_replace_decorator_with_function_pointer():
    # In downstream package which want's to overwrite the API
    @set_config('mara_config.tests.test_config.something', include_original_function=True)
    def replacement_for_something(argument: str = None, original_function=None) -> str:
        assert callable(original_function)
        tmp = original_function(argument)
        return tmp + (argument or 'y')

    assert 'xy' == something()
    assert 'xABC' == something("ABC")


def test_replace_function():
    def replacement_for_something(argument: str = None) -> str:
        return argument or 'y'

    set_config('mara_config.tests.test_config.something', function=replacement_for_something)

    assert 'y' == something()
    assert 'ABC' == something("ABC")


def test_replace_function_with_non_function():
    with pytest.raises(AssertionError):
        set_config('mara_config.tests.test_config.something', function="something")


def test_needs_set_without_set():
    @declare_config(needs_set=True)
    def _tester(argument: str = None) -> str:
        return "x"

    with pytest.raises(NotImplementedError):
        _tester()


def test_needs_set_with_set():
    @declare_config(config_name='random__test_needs_set_with_set', needs_set=True)
    def _tester(argument: str = None) -> str:
        return "x"

    @set_config('random__test_needs_set_with_set')
    def _replacement(argument: str = None) -> str:
        return "y"

    assert _tester() == 'y'

def test_needs_set_with_set_and_include_parent():
    @declare_config(config_name='random__test_needs_set_with_set_and_include_parent', needs_set=True)
    def _tester(argument: str = None) -> str:
        return "x"

    with pytest.raises(NotImplementedError):
        _tester()

    @set_config('random__test_needs_set_with_set_and_include_parent', include_original_function=True)
    def _replacement(argument: str = None, original_function=None) -> str:
        ret = original_function()
        return "y"+ret

    assert _tester() == 'yx'

def test_warn_on_use_replace_decorator_twice(caplog):
    # In downstream package which want's to overwrite the API
    caplog.set_level(logging.INFO)

    @set_config('mara_config.tests.test_config.something')
    def replacement_for_something(argument: str = None) -> str:
        return argument or 'y'

    @set_config('mara_config.tests.test_config.something')
    def replacement_for_something2(argument: str = None) -> str:
        return 'z'

    assert len(caplog.records) == 1
    assert "already replaced" in caplog.records[0].message

    assert 'z' == something()
    assert 'z' == something("ABC")


def test_add_config_from_environment():
    import os
    os.environ['mara_mara_config__tests__test_config__without_args'] = 'y'

    assert 'x' == without_args()

    add_config_from_environment()

    assert 'y' == without_args()
