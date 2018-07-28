# -*- coding: cp936 -*-
"""
这是迭代模块
"""


def print_lol(the_list):
    """
    迭代函数，自调用
    :param the_list: 
    :return: null
    """
    for each_list in the_list:
        if isinstance(each_list,list) :
            print_lol(each_list)
        else :
            print(each_list)
