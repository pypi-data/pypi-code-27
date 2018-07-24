# -*- coding: utf-8 -*-

"""Tests for PyBEL-CX entry points."""

import unittest

from pkg_resources import iter_entry_points


class TestEntryPoints(unittest.TestCase):
    """A class wrapping entry points tests."""

    def test_entry_points(self):
        """Test that the functions from PyBEL-CX can be loaded."""
        entry_points = list(iter_entry_points(group='pybel.converter'))
        self.assertNotEqual(0, len(entry_points))

        entry_point_names = {entry_point.name for entry_point in entry_points}
        self.assertIn('to_ndex', entry_point_names)
