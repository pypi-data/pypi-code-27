# -*- coding:utf-8 -*
"""
author: rontgen
Date: 2018-08-02
Function Description: 
    1. convert between Simple Chinese, Hong Kong Traditional Chinese and Traditional Chinese
"""

import opencc
"""
'hk2s': Traditional Chinese (Hong Kong standard) to Simplified Chinese

's2hk': Simplified Chinese to Traditional Chinese (Hong Kong standard)

's2t': Simplified Chinese to Traditional Chinese

's2tw': Simplified Chinese to Traditional Chinese (Taiwan standard)

's2twp': Simplified Chinese to Traditional Chinese (Taiwan standard, with phrases)

't2hk': Traditional Chinese to Traditional Chinese (Hong Kong standard)

't2s': Traditional Chinese to Simplified Chinese

't2tw': Traditional Chinese to Traditional Chinese (Taiwan standard)

'tw2s': Traditional Chinese (Taiwan standard) to Simplified Chinese

'tw2sp': Traditional Chinese (Taiwan standard) to Simplified Chinese (with phrases)
"""

class CNConvert():
    def __init__(self):
        self._s2tcvt = opencc.OpenCC('s2t')
        self._t2scvt = opencc.OpenCC('t2s')
        self._s2twcvt = opencc.OpenCC('s2tw')
        self._s2twpcvt = opencc.OpenCC('s2twp')
        self._s2hkcvt = opencc.OpenCC('s2hk')
        self._hk2scvt = opencc.OpenCC('hk2s')
        self._tw2scvt = opencc.OpenCC('tw2s')
        self._tw2spcvt = opencc.OpenCC('tw2sp')
        self._t2hkcvt = opencc.OpenCC('t2hk')
        self._t2twcvt = opencc.OpenCC('t2tw')


    def s2t(self, strs):
        if strs != "":
            return self._s2tcvt.convert(strs)
        else:
            return ""

    def t2s(self, strs):
        if strs != "":
            return self._t2scvt.convert(strs)
        else:
            return ""

    def s2tw(self, strs):
        if strs != "":
            return self._s2twcvt.convert(strs)
        else:
            return ""

    def s2twp(self, strs):
        if strs != "":
            return self._s2twpcvt.convert(strs)
        else:
            return ""

    def s2hk(self, strs):
        if strs != "":
            return self._s2hkcvt.convert(strs)
        else:
            return ""

    def hk2s(self, strs):
        if strs != "":
            return self._hk2scvt.convert(strs)
        else:
            return ""

    def tw2s(self, strs):
        if strs != "":
            return self._tw2scvt.convert(strs)
        else:
            return ""

    def tw2sp(self, strs):
        if strs != "":
            return self._tw2spcvt.convert(strs)
        else:
            return ""

    def t2hk(self, strs):
        if strs != "":
            return self._t2hkcvt.convert(strs)
        else:
            return ""

    def t2tw(self, strs):
        if strs != "":
            return self._t2twcvt.convert(strs)
        else:
            return ""