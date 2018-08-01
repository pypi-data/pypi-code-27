# -*- coding:utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__) + '/../..')

from xc_ip_info.ip_info import IPSearcher


class TestIpInfo(unittest.TestCase):
    """
    ip_info 测试
    """

    def test_ip_info(self):
        # 北京ip，能够返回正确汉字
        res = IPSearcher.search('123.125.71.38')
        self.assertEqual(res['province'].encode('utf8'), '北京')

        # 新疆ip，默认敏感
        res = IPSearcher.validate('61.128.101.255')
        self.assertEqual(res['access'], 2)

        # 北京ip
        res = IPSearcher.validate('123.125.71.38')
        self.assertEqual(res['access'], 1)

        ip_result = IPSearcher.validate("120.68.241.255")
        self.assertEqual(ip_result[u'access'], 2)
        self.assertEqual(ip_result[u'type'], u'sensitive')
        self.assertEqual(ip_result[u'reason'], u'province 新疆 is sensitive')

        # 杭州 ip测试用例
        ip_result = IPSearcher.validate("36.18.192.1")
        self.assertEqual(ip_result[u'access'], 1)
        self.assertEqual(ip_result[u'type'], u'normal')

        # 阿根廷 外国测试
        res = IPSearcher.validate('200.89.143.138')
        self.assertEqual(res['country'], u'阿根廷')
        self.assertEqual(res['reason'], u'foreign is sensitive')
        self.assertEqual(res['access'], 2)

        # 异常测试，ip为空
        ip_result = IPSearcher.validate("")
        self.assertEqual(ip_result[u'access'], 1)
        self.assertEqual(ip_result[u'type'], u'normal')

        # 异常测试，ip格式不正确
        ip_result = IPSearcher.validate("12345")
        self.assertEqual(ip_result[u'access'], 1)
        self.assertEqual(ip_result[u'type'], u'normal')

        # 新疆测试
        ip_result = IPSearcher.validate("222.80.143.138")
        self.assertEqual(ip_result[u'access'], 2)
        self.assertEqual(ip_result[u'type'], u'sensitive')
        self.assertEqual(ip_result[u'reason'], u'province 新疆 is sensitive')

        # ipip不命中测试，额，找不到例子
        ip_result = IPSearcher.validate("200.89.143.138")

        # 淘宝ip，西藏
        res = IPSearcher.search_from_taobao('124.31.255.254')
        self.assertEqual(res['province'], u'西藏')
        self.assertEqual(res['country'], u'中国')

        # 淘宝ip，西藏，第二次同ip测试从内存读
        res = IPSearcher.search_from_taobao('124.31.255.254')
        self.assertEqual(res['province'], u'西藏')
        self.assertEqual(res['country'], u'中国')

        # 淘宝ip，ip为空
        ip_result = IPSearcher.search_from_taobao("")
        self.assertEqual(ip_result, {})

        # 淘宝ip，ip格式不正确
        ip_result = IPSearcher.search_from_taobao("12345")
        self.assertEqual(ip_result, {})

        # 淘宝ip，外国country字段正常返回
        res = IPSearcher.search_from_taobao('200.89.143.138')
        self.assertEqual(res['country'], u'阿根廷')


if __name__ == '__main__':

    # 运行所有用例
    unittest.main()
