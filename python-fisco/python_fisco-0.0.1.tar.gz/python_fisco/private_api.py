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
    def __init__(self, api_key, api_secret):
        self.end_point = 'https://api.fcce.jp/tapi'
        self.api_key = api_key
        self.api_secret = api_secret

    def post_query(self, method: str, payload: dict) -> dict:
        payload['method'] = method
        payload['nonce'] = str(time.time())
        headers = PrivateApi.make_header(
            urlencode(payload).encode('utf8'), self.api_key, self.api_secret)
        response = requests.post(self.end_point, headers=headers, data=payload)
        return PrivateApi.error_parser(response.json())

    def get_info(self) -> dict:
        return self.post_query(inspect.stack()[0][3], {})

    def trade_history(self, **options) -> dict:
        query = ApiValidator.assign_optionals(inspect.stack()[0][3], {},
                                              options)
        return self.post_query(inspect.stack()[0][3], query)

    def active_orders(self, **options) -> dict:
        query = ApiValidator.assign_optionals(inspect.stack()[0][3], {},
                                              options)
        return self.post_query(inspect.stack()[0][3], query)

    def trade(self, currency_pair: str, action: str, price: str, amount: str,
              **options) -> dict:
        params = dict(
            currency_pair=currency_pair,
            action=action,
            price=price,
            amount=amount)
        query = ApiValidator.assign_optionals(inspect.stack()[0][3], params,
                                              options)
        return self.post_query(inspect.stack()[0][3], query)

    def cancel_order(self, order_id: int) -> dict:
        query = dict(order_id=order_id)
        return self.post_query(inspect.stack()[0][3], query)

    def withdraw(self, currency: str, address: str, amount: Decimal,
                 **options) -> dict:
        params = dict(currency=currency, address=address, amount=amount)
        query = ApiValidator.assign_optionals(inspect.stack()[0][3], params,
                                              options)
        return self.post_query(inspect.stack()[0][3], query)

    def deposit_history(self, currency: str, **options) -> dict:
        query = ApiValidator.assign_optionals(
            inspect.stack()[0][3], dict(currency=currency), options)
        return self.post_query(inspect.stack()[0][3], query)

    def withdraw_history(self, currency: str, **options) -> dict:
        query = ApiValidator.assign_optionals(
            inspect.stack()[0][3], dict(currency=currency), options)
        return self.post_query(inspect.stack()[0][3], query)

    @staticmethod
    def sign_request(key, query):
        return hmac.new(bytes(key, 'latin-1'), query,
                        hashlib.sha512).hexdigest()

    @staticmethod
    def make_header(query, api_key, api_secret):
        return {
            'Key': api_key,
            'Sign': PrivateApi.sign_request(api_secret, query),
        }

    @staticmethod
    def error_parser(response):
        if response['success'] == 1:
            return response['return']
        else:
            raise FiscoServerException(response['error'])
