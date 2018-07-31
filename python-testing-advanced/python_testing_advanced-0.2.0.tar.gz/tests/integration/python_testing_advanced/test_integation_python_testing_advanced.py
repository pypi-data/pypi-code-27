# -*- coding: utf-8 -*-


"""Integration Tests for `python_testing_advanced` package."""


from python_testing_advanced import python_testing_advanced


def test_init(mocker):
    """python_testing_advanced :: Integration :: python_testing_advanced :: init"""  # nopep8

    mocker.patch.object(python_testing_advanced, 'help')
    mocker.patch.object(python_testing_advanced, '__name__', '__main__')

    python_testing_advanced.init()

    python_testing_advanced.help.assert_called_once()
