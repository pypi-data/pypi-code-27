#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/2/26

"""
    desc:pass
"""
import unittest

import math


import dueros.Log as log
import logging
class BaseTest(object):

    def test_sqrt(self):
        self.assertEqual(math.sqrt(4) * math.sqrt(4), 4)


if __name__ == "__main__":
    # unittest.main()

    a = 11.09
    print(str(a))
    data = {}
    data['payload']['chargeBaiduPay']['authorizeAttributes']['authorizationAmount'][
        'amount'] = str(11)
