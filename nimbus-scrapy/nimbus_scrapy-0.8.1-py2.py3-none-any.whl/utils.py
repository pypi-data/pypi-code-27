# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import re
import logging
import json
from functools import wraps
from datetime import datetime, timedelta, date
from dateutil import parser
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity
from scrapy.loader.processors import Compose, SelectJmes, MergeDict

__all__ = [
    "TakeSecond",
    "filter_trim",
    "filter_int",
    "filter_datetime",
]

INT = re.compile(r'\d')


class TakeSecond(object):

    def __call__(self, values):
        if len(values) >= 2:
            return values[1]


def filter_price(value):
    if value.isdigit():
        return value


def filter_trim(value):
    if isinstance(value, (tuple, list)) and len(value) > 0:
        return value[0].strip()
    elif isinstance(value, basestring):
        return value.strip()
    return value


def filter_int(value):
    if isinstance(value, basestring):
        value = INT.findall(value)
        return value
    return value


def filter_datetime(value):
    if isinstance(value, basestring):
        value = value.replace('[', '').replace(']', '')
        value = value.strip()
        value = parser.parse(value)
        return value
    return value





