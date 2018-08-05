import unittest

from . import cli


class TestErrorChecking(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_bounds_checking(self):
        cli.check_fails(
            self, 'pyrandomsearch.pyrandomsearch',
            args=[
                '--dimensionality=0',
                '',
            ],
            stdin='')
        cli.check_fails(
            self, 'pyrandomsearch.pyrandomsearch',
            args=[
                '--stale-threshold=-1',
                '',
            ],
            stdin='')
        cli.check_fails(
            self, 'pyrandomsearch.pyrandomsearch',
            args=[
                '--stale-count=0',
                '',
            ],
            stdin='')
        cli.check_fails(
            self, 'pyrandomsearch.pyrandomsearch',
            args=[
                '--num-proposals=0',
                '',
            ],
            stdin='')
