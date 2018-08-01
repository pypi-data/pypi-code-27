# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 9:49
# @Author  : yangyong
# @Email   : yangyong@findourlove.com
# @File    : three.py
# @Software: PyCharm
def raise_with_traceback(exc_type, traceback, *args, **kwargs):
    """
    用现有的“traceback”来提出“exc类型”的新异常。
    """
    raise exc_type(*args, **kwargs).with_traceback(traceback)