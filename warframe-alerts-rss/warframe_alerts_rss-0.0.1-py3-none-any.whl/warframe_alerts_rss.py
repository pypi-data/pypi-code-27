#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Tong Miao (illemonati)'
__version__ = "0.0.1"
__status__ = 'Prototype'
__email__ = "tonymiaotong@tioft.tech"

import feedparser
from .WarframeAlert import WarframeAlert

class WarframeAlertsRss():
    def __init__(self,rss_url='http://content.warframe.com/dynamic/rss.php'):
        self.warframe_rss = feedparser.parse(rss_url)

    def get_alerts(self):
        alert_list = []
        feed_entries = self.warframe_rss.entries
        for entry in feed_entries:
            # print(entry)
            title= entry.title
            type = entry.author
            extra = ''
            time_created = entry.published_parsed
            try:
                extra = entry.summary
            except Exception as e:
                pass
            # print(entry)
            alert_list.append(WarframeAlert(title,type,extra, time_created, raw=entry))
        return alert_list
