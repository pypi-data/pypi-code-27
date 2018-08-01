# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 9:50
# @Author  : yangyong
# @Email   : yangyong@findourlove.com
# @File    : two.py
# @Software: PyCharm
def raise_with_traceback(exc_type, traceback, *args, **kwargs):
    raise exc_type(*args, **kwargs), None, traceback