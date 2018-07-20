# -*- coding: utf-8 -*-

"""Test invalid input."""

from __future__ import absolute_import

from .check import Check

from proselint.tools import lint as lint


class TestInvalidInput(Check):
    """Test class for invalid input."""

    __test__ = True

    def test_invalid_utf8(self):
        """Test that linter runs on input with invalid UTF-8 characters."""
        invalid_text = """Ó """
        assert lint(invalid_text)
