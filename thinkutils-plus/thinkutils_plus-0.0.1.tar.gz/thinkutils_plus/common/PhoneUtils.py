#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

class PhoneUtils(object):
    @classmethod
    def get_imsi_operator(cls, szImsi):
        if szImsi is None or len(szImsi) < 5:
            return 4

        if szImsi.startswith("46000") or szImsi.startswith("46002") or szImsi.startswith("46007"):
            return 2  #CMCC
        elif szImsi.startswith("46001"):
            return 1 #CUCC
        elif szImsi.startswith("46003"):
            return 3 #CTCC
        else:
            return 4
