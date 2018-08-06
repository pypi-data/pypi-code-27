import pytest

import conlog
# import utils


def test_start_with_non_existent_kwarg():
    """Test that using start with an unknown kwarg throws a
    TypeError.
    """
    with pytest.raises(TypeError):
        conlog.start(unknown_kw='Should throw TypeError')


def test_logger_with_default_values():
    """Test to make sure that Logger root instance is setup
    with default values.
    """
    log = conlog.start()
    assert log.name == 'root'
    assert log.level == 20  # Level 20 = INFO Level
    #
    # TODO: Come up with ways to test for other default values?
    #
