#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2018 smapira
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Fisco Private API Wrapper.

This module handling API.

See:
   https://fcce.jp/api-docs/trade-api
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import hashlib
import inspect
from decimal import Decimal
from logging import getLogger
from urllib.parse import urlencode
import hmac
import requests
import time
from python_fisco.error import FiscoServerException
from .api_validator import ApiValidator
logger = getLogger(__name__)


class PrivateApi(object):
    """Fisco Public Api class.

    Attributes:
        end_point (string): 'https://api.fcce.jp/tapi'
        api_key (string):
        api_secret (string):
    """
    def __init__(self, api_key, api_secret):
        self.end_point = 'https://api.fcce.jp/tapi'
        self.api_key = api_key
        self.api_secret = api_secret

    def post_query(self, method: str, payload: dict) -> dict:
        """Post query
        API Type HTTP Private API
        :param  method: Designate "get_info",
          "trade_history", "active_orders", "trade", "cancel_order",
          "withdraw", "deposit_history" or "withdraw_history".:
        :type method: str.
        :param  payload:
        :type payload: dict.
        :return: dict
        """
        payload['method'] = method
        payload['nonce'] = str(time.time())
        headers = PrivateApi.make_header(
            urlencode(payload).encode('utf8'), self.api_key, self.api_secret)
        response = requests.post(self.end_point, headers=headers, data=payload)
        return PrivateApi.error_parser(response.json())

    def get_info(self) -> dict:
        """Get information
        API Type HTTP Private API
        :return: dict
        """
        return self.post_query(inspect.stack()[0][3], {})

    def get_trade_history(self, **options) -> dict:
        """Get trade history
        API Type HTTP Private API
        :return: dict
        """
        query = ApiValidator.assign_optionals(inspect.stack()[0][3], {},
                                              options)
        return self.post_query(inspect.stack()[0][3], query)

    def get_active_orders(self, **options) -> dict:
        """Get active orders
        API Type HTTP Private API
        :return: dict
        """
        query = ApiValidator.assign_optionals(inspect.stack()[0][3], {},
                                              options)
        return self.post_query(inspect.stack()[0][3], query)

    def trade(self, currency_pair: str, action: str, price: Decimal, amount: Decimal,
              **options) -> dict:
        """Request trade
        API Type HTTP Private API
        :param  currency_pair: Designate "btc_jpy", "mona_jpy" or "mona_btc".
        :type currency_pair: str.
        :param  action:  Designate "bid", or "ask".
        :type action: str.
        :param  price:
        :type price: Decimal.
        :param  amount:
        :type amount: Decimal.
        :return: dict
        """
        params = dict(
            currency_pair=currency_pair,
            action=action,
            price=price,
            amount=amount)
        query = ApiValidator.assign_optionals(inspect.stack()[0][3], params,
                                              options)
        return self.post_query(inspect.stack()[0][3], query)

    def cancel_order(self, order_id: int) -> dict:
        """Cancel order
        API Type HTTP Private API
        :param  order_id:
        :type order_id: int.
        :return: dict
        """
        query = dict(order_id=order_id)
        return self.post_query(inspect.stack()[0][3], query)

    def withdraw(self, currency: str, address: str, amount: Decimal,
                 **options) -> dict:
        """Withdraw
        API Type HTTP Private API
        :param  currency: Designate "btc", or "mona".
        :type currency: str.
        :param  address:
        :type address: str.
        :param  amount:
        :type amount: Decimal.
        :return: dict
        """
        params = dict(currency=currency, address=address, amount=amount)
        query = ApiValidator.assign_optionals(inspect.stack()[0][3], params,
                                              options)
        return self.post_query(inspect.stack()[0][3], query)

    def get_deposit_history(self, currency: str, **options) -> dict:
        """Get deposit history
        API Type HTTP Private API
        :param  currency: Designate "btc", "jpy", or "mona".
        :type currency: str.
        :return: dict
        """
        query = ApiValidator.assign_optionals(
            inspect.stack()[0][3], dict(currency=currency), options)
        return self.post_query(inspect.stack()[0][3], query)

    def get_withdraw_history(self, currency: str, **options) -> dict:
        """Get withdraw history
        API Type HTTP Private API
        :param  currency: Designate "btc", "jpy", or "mona".
        :type currency: str.
        :return: dict
        """
        query = ApiValidator.assign_optionals(
            inspect.stack()[0][3], dict(currency=currency), options)
        return self.post_query(inspect.stack()[0][3], query)

    @staticmethod
    def sign_request(key: str, query: str) -> str:
        return hmac.new(bytes(key, 'latin-1'), query,
                        hashlib.sha512).hexdigest()

    @staticmethod
    def make_header(query: str, api_key: str, api_secret: str) -> dict:
        return {
            'Key': api_key,
            'Sign': PrivateApi.sign_request(api_secret, query),
        }

    @staticmethod
    def error_parser(response: dict) -> dict:
        if response['success'] == 1:
            return response['return']
        else:
            raise FiscoServerException(response['error'])
