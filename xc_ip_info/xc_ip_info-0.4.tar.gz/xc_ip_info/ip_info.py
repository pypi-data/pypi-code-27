# coding=utf-8
"""
检查ip合法性，或者查询ip信息
"""
from .lib.ipip import IP
import json
import logging
import os
import re
import requests


class IPSearcher(object):
    """
    ip信息查询类，IP类的操作封装
    因为全局需要共享一个IP类，可以写成单例，甚至可以不用类。但是__rules和__initialized需要封装置为静态的私有变量，所以用类，并且此封装类无需有多个对象，所以操作都是静态的
    """
    TAOBAO_IP_MAX_COUNT = 100000
    __taobao_ip_infos = {}
    __rules = {}
    __initialized = 0
    __filter_foreign_country = False
    __compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')

    @staticmethod
    def prepare(path, rules_str='{}', filter_foreign_country=False):
        """
        初始化内部数据
        :param path: 文件路径，rules_str：json格式的不合法城市和省份名，汉字
        异常：path打不开IP不变；json解析失败等同于空rules
        :param rules_str: 地区黑名单
        :param filter_foreign_country: 是否过滤外国IP
        :return:
        """
        try:
            IP.load(path)
        except Exception as e:
            logging.error("IPSearcher failed to open file, use original instead, e:%s" % str(e))
        try:
            IPSearcher.__rules = json.loads(rules_str)
        except Exception as e:
            logging.error("IPSearcher failed to load rules_str, use empty instead, e:%s" % str(e))
            IPSearcher.__rules = {}
        IPSearcher.__initialized = 1
        IPSearcher.__filter_foreign_country = filter_foreign_country

    @classmethod
    def search_from_taobao(cls, ip):
        try:
            if not ip:
                logging.warn("search ip info from taobao failed, ip: %s, error: ip is empty" % ip)
                return {}
            if not cls.__compile_ip.match(str(ip)):
                logging.warn("search ip info from taobao failed, ip: %s, error: ip format is not valid" % ip)
                return {}

            if str(ip) in cls.__taobao_ip_infos:
                return cls.__taobao_ip_infos[str(ip)]

            taobao_url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + str(ip)
            res = requests.get(taobao_url, timeout=0.2).json()
            if not isinstance(res, dict) or not isinstance(res.get('data', ''), dict) or not res['data'].get('city', '')\
                or not res['data'].get('region', '') or not res['data'].get('country', ''):
                logging.warn("search ip info from taobao failed, ip: %s, error: taobao res is not complete" % ip)
                return {}
            ret = {'country': res['data']['country'], 'province': res['data']['region'], 'city': res['data']['city']}
            if len(cls.__taobao_ip_infos) > cls.TAOBAO_IP_MAX_COUNT:
                logging.info('too many taobao_ip_infos, reset the dict')
                cls.__taobao_ip_infos = {}
            cls.__taobao_ip_infos[str(ip)] = ret
            return ret
        except Exception as e:
            logging.warn("search ip info from taobao failed, ip: %s, error: %s" % (ip, str(e)))
            return {}

    @staticmethod
    def search(ip):
        """
        根据ip查询信息
        :param ip: ipv4字符串
        :return ip格式错误、未初始化或者找不到返回{}
        """
        if not IPSearcher.__initialized:
            data_file_path = os.path.realpath(__file__).split('xc_ip_info/')[0] + "xc_ip_info/data/17monipdb.dat"
            IPSearcher.prepare(data_file_path, '{"province": ["新疆"]}', True)
            logging.info("Initialized IPSearch")
        try:
            ipinfo = IP.find(ip)
        except Exception as e:
            return {}
        if ipinfo == "N/A":
            return {}
        ipinfo = ipinfo.split("\t")
        res = {'country': '', 'province': '', 'city': ''}
        # IP.find返回的长度不一定
        if len(ipinfo) >= 1:
            res['country'] = ipinfo[0]
        if len(ipinfo) >= 2:
            res['province'] = ipinfo[1]
        if len(ipinfo) >= 3:
            res['city'] = ipinfo[2]

        return res

    @staticmethod
    def validate(ip):
        """
        判断ip是否合法
        :param ip: ipv4字符串
        :return wiki：http://doc.ixiaochuan.cn/pages/viewpage.action?pageId=853396
        """
        res = {'type': 'normal', 'access': 1, 'reason': '', 'ip': ip}
        info = IPSearcher.search(ip)
        if not info:
            return res

        # 开启过滤外国IP
        res.update(info)
        if IPSearcher.__filter_foreign_country and info.get('country') != u'中国':
            res.update({'type': 'sensitive', 'access': 2, 'reason': 'foreign is sensitive'})
            return res

        # 判断是否是敏感地区
        for name, entities in IPSearcher.__rules.items():
            if info.get(name, '') in entities:
                res.update({'type': 'sensitive', 'access': 2, 'reason': name + ' ' + info[name] + ' is sensitive'})
                break
        return res
