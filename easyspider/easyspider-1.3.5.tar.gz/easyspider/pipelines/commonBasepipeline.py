# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2018-03-05 19:20:28
# @Last Modified by:   hang.zhang
# @Last Modified time: 2018-03-18 20:45:55
from easyspider.pipelines.commonpipeline import commonpipeline
from easyspider.utils.tools import get_time
import socket

flat = (lambda L: sum(map(flat, L), []) if isinstance(L, list) or isinstance(L, tuple) else [L])


class commonBasepipeline(commonpipeline):

    def _process_item(self, item, spider, response):
        item["crawled_time"] = get_time()
        item["spider"] = spider.name
        # 多机器抓取用来标志是来源于哪台机器
        try:
            item["crawled_server"] = ";".join(flat(socket.gethostbyname_ex(socket.gethostname())))
        except Exception:
            # 某些情况下可能会出错
            item["crawled_server"] = socket.gethostname()
        # item["crawled_url"] = response.url
        return item
