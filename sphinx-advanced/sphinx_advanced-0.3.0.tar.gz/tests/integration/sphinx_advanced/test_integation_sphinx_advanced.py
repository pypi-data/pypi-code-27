# -*- coding: utf-8 -*-


"""Integration Tests for `sphinx_advanced` package."""


from sphinx_advanced import sphinx_advanced


def test_init(mocker):
    """sphinx_advanced :: Integration :: sphinx_advanced :: init"""

    mocker.patch.object(sphinx_advanced, 'help')
    mocker.patch.object(sphinx_advanced, '__name__', '__main__')

    sphinx_advanced.init()

    sphinx_advanced.help.assert_called_once()
