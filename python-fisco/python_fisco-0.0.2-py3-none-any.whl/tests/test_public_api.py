from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import vcr
from unittest import TestCase
from logging import getLogger
from python_fisco.public_api import PublicApi
logger = getLogger(__name__)
vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir='fixtures/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)


class FiscPublicTests(TestCase):
    def setUp(self):
        self.public = PublicApi()

    @vcr.use_cassette()
    def test_ticker(self):
        response = self.public.get_ticker('btc_jpy')
        self.assertTrue('ask' in response)
        self.assertTrue('bid' in response)
        self.assertTrue('high' in response)
        self.assertTrue('last' in response)
        self.assertTrue('low' in response)
        self.assertTrue('volume' in response)
        self.assertTrue('vwap' in response)

    @vcr.use_cassette()
    def test_last_price(self):
        response = self.public.get_last_price('btc_jpy')
        self.assertTrue('last_price' in response)

    @vcr.use_cassette()
    def test_trades(self):
        response = self.public.get_trades('btc_jpy')
        self.assertTrue('amount' in response[0])
        self.assertTrue('currency_pair' in response[0])
        self.assertTrue('date' in response[0])
        self.assertTrue('price' in response[0])
        self.assertTrue('tid' in response[0])
        self.assertTrue('trade_type' in response[0])

    @vcr.use_cassette()
    def test_depth(self):
        response = self.public.get_depth('btc_jpy')
        self.assertTrue('asks' in response)
        self.assertTrue('bids' in response)


if __name__ == '__main__':
    unittest.main()
