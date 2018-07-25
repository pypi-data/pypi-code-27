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

from python_fisco.error import FiscoApiValidationError
from cerberus import Validator


class ApiValidator:
    def __init__(self):
        pass

    @staticmethod
    def does_valid_query(method: str, query: dict):
        schema = {
            x: ApiValidator.DEFAULT_SCHEMA[x]
            for x in ApiValidator.GROUP_METHODS[method]
        }
        validator = Validator(schema)
        if validator.validate(query) is False:
            raise FiscoApiValidationError(str(validator.errors))

    @staticmethod
    def assign_optionals(method: str, query: dict, options: dict) -> dict:
        schema = ApiValidator.DEFAULT_SCHEMA
        if method == 'trade_history':
            schema['currency_pair']['required'] = False
        if method == 'trade':
            schema['currency_pair']['required'] = True
        for k in [
                x for x in schema.keys()
                if 'required' not in ApiValidator.DEFAULT_SCHEMA[x]
        ]:
            if options.get(str(k)) is None:
                continue
            query[k] = options.get(str(k))
        ApiValidator.does_valid_query(method, query)
        return query

    GROUP_METHODS = {
        'get_info': [],
        'trade_history': [
            'from', 'count', 'from_id', 'end_id', 'order', 'since', 'end',
            'currency_pair'
        ],
        'active_orders': ['currency_pair'],
        'trade': ['currency_pair', 'action', 'price', 'amount', 'limit'],
        'cancel_order': ['order_id'],
        'withdraw': ['currency', 'address', 'amount', 'opt_fee'],
        'deposit_history': [
            'currency', 'from', 'count', 'from_id', 'end_id', 'order', 'since',
            'end'
        ],
        'withdraw_history': [
            'currency', 'from', 'count', 'from_id', 'end_id', 'order', 'since',
            'end'
        ],
        'get_ticker': ['pair'],
        'get_last_price': ['pair'],
        'get_trades': ['pair'],
        'get_depth': ['pair'],
    }

    DEFAULT_SCHEMA = {
        'from': {
            'nullable': True,
            'type': 'integer',
        },
        'count': {
            'nullable': True,
            'type': 'integer'
        },
        'from_id': {
            'nullable': True,
            'type': 'integer'
        },
        'end_id': {
            'nullable': True,
            'type': ['string', 'integer']
        },
        'order': {
            'nullable': True,
            'type': 'string',
            'allowed': ['ASC', 'DESC', None]
        },
        'since': {
            'nullable': True,
            'type': 'integer'
        },
        'end': {
            'nullable': True,
            'type': ['string', 'integer']
        },
        'currency_pair': {
            'nullable': True,
            'type': 'string'
        },
        'action': {
            'required': True,
            'type': 'string',
            'allowed': ['bid', 'ask', None]
        },
        'price': {
            'required': True,
            'type': 'number'
        },
        'amount': {
            'required': True,
            'type': 'number'
        },
        'limit': {
            'nullable': True,
            'type': 'number'
        },
        'order_id': {
            'required': True,
            'type': 'integer'
        },
        'currency': {
            'required': True,
            'type': 'string',
            'allowed': ['btc', 'mona', 'jpy', None]
        },
        'address': {
            'required': True,
            'type': 'string'
        },
        'opt_fee': {
            'nullable': True,
            'type': 'number'
        },
        'pair': {
            'required': True,
            'type': 'string',
            'allowed': ['btc_jpy', 'mona_jpy', 'mona_btc']
        }
    }
