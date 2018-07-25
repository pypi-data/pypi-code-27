from __future__ import absolute_import, division, print_function, unicode_literals

import os
from typing import Union
from os.path import join, dirname
from dotenv import load_dotenv
import unittest
import vcr
from unittest import TestCase
from logging import getLogger

from python_fisco.private_api import PrivateApi
logger = getLogger(__name__)
vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir='fixtures/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)
dotenv_path: Union[bytes, str] = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)


class FiscPublicTests(TestCase):
    def setUp(self):
        self.private = PrivateApi(
            os.environ.get('FCCE_KEY'), os.environ.get('FCCE_SECRET'))

    @vcr.use_cassette()
    def test_get_info(self):
        response = self.private.get_info()
        self.assertTrue('deposit' in response)
        self.assertTrue('btc' in response['deposit'])
        self.assertTrue('jpy' in response['deposit'])
        self.assertTrue('mona' in response['deposit'])
        self.assertTrue('funds' in response)
        self.assertTrue('btc' in response['funds'])
        self.assertTrue('jpy' in response['funds'])
        self.assertTrue('mona' in response['funds'])
        self.assertTrue('open_orders' in response)
        self.assertTrue('rights' in response)
        self.assertTrue('id_info' in response['rights'])
        self.assertTrue('info' in response['rights'])
        self.assertTrue('personal_info' in response['rights'])
        self.assertTrue('trade' in response['rights'])
        self.assertTrue('withdraw' in response['rights'])
        self.assertTrue('server_time' in response)
        self.assertTrue('trade_count' in response)

    @vcr.use_cassette()
    def test_trade_history(self):
        response = self.private.get_trade_history()
        self.assertTrue(response == {})

    @vcr.use_cassette()
    def test_active_orders(self):
        response = self.private.get_active_orders()
        self.assertTrue(response == {})

    @vcr.use_cassette()
    def test_trade(self):
        self.assertRaises(
            Exception,
            self.private.trade,
            currency_pair='btc_jpy',
            action='ask',
            price='70000',
            amount='0.001')

    @vcr.use_cassette()
    def test_cancel_order(self):
        self.assertRaises(Exception, self.private.trade, order_id=1)

    @vcr.use_cassette()
    def test_withdraw(self):
        self.assertRaises(
            Exception,
            self.private.withdraw,
            currency='btc',
            address='address',
            amount='0.001')

    @vcr.use_cassette()
    def test_deposit_history(self):
        response = self.private.get_deposit_history('btc')
        self.assertTrue(response == {})

    @vcr.use_cassette()
    def test_withdraw_history(self):
        response = self.private.get_withdraw_history('btc')
        self.assertTrue(response == {})


if __name__ == '__main__':
    unittest.main()
