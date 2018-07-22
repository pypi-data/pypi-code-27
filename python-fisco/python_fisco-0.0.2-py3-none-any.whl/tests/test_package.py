from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import vcr
from unittest import TestCase
from logging import getLogger
from python_fisco import *

logger = getLogger(__name__)
vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir='fixtures/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)


class PackageTest(TestCase):

    @vcr.use_cassette()
    def test_import(self):
        response = FiscoPublic().get_ticker('btc_jpy')
        self.assertTrue('ask' in response)


if __name__ == '__main__':
    unittest.main()
