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

"""Fisco Public API Wrapper.

This module handling API.

See:
   https://fcce.jp/api-docs
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import inspect
from logging import getLogger
import requests

from .api_validator import ApiValidator

logger = getLogger(__name__)


class PublicApi(object):
    """Fisco Public Api class.

    Attributes:
        end_point (string): 'https://api.fcce.jp/api/1'
    """
    def __init__(self):
        self.end_point = 'https://api.fcce.jp/api/1'

    @staticmethod
    def request_query(url: str, pair: str) -> dict:
        response = requests.get(url + pair)
        return PublicApi.error_parser(response.json())

    def get_ticker(self, pair: str) -> dict:
        """Get ticker
        API Type HTTP Public API
        :param  pair: Designate "btc_jpy", "mona_jpy" or "mona_btc".:
        :type pair: str.
        :return: dict
        """
        ApiValidator.assign_optionals(inspect.stack()[0][3], {'pair': pair}, {})
        return PublicApi.request_query(self.end_point + '/ticker/', pair)

    def get_last_price(self, pair: str) -> dict:
        """Get last price
        API Type HTTP Public API
        :param  pair: Designate "btc_jpy", "mona_jpy" or "mona_btc".:
        :type pair: str.
        :return: dict
        """
        ApiValidator.assign_optionals(inspect.stack()[0][3], {'pair': pair}, {})
        return PublicApi.request_query(self.end_point + '/last_price/', pair)

    def get_trades(self, pair: str) -> dict:
        """Get trades
        API Type HTTP Public API
        :param  pair: Designate "btc_jpy", "mona_jpy" or "mona_btc".:
        :type pair: str.
        :return: dict
        """
        ApiValidator.assign_optionals(inspect.stack()[0][3], {'pair': pair}, {})
        return PublicApi.request_query(self.end_point + '/trades/', pair)

    def get_depth(self, pair: str) -> dict:
        """Get depth
        API Type HTTP Public API
        :param  pair: Designate "btc_jpy", "mona_jpy" or "mona_btc".:
        :type pair: str.
        :return: dict
        """
        ApiValidator.assign_optionals(inspect.stack()[0][3], {'pair': pair}, {})
        return PublicApi.request_query(self.end_point + '/depth/', pair)

    @staticmethod
    def error_parser(response):
        return response
