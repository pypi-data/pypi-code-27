#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Tong Miao (illemonati)'
__version__ = "0.0.1"
__status__ = 'Prototype'
__email__ = "tonymiaotong@tioft.tech"


class WarframeAlert():
    def __init__(self, title, type, extra, time_created, raw=None):
        self.title = title
        self.type = type
        self.extra = extra
        self.time_created = time_created
        self.raw = raw

    def __str__(self):
        return str(self.raw)

    def __unicode__(self):
        return unicode(str(self.raw))
    def __repr__(self):
        return str(self.raw)
