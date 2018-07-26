#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhangyue'

from datetime import datetime
from django import template
from django.conf import settings
from bee_django_report.utils import get_user_name
from bee_django_report.exports import filter_local_datetime

register = template.Library()


# 求两个值的差的绝对值
@register.filter
def get_difference_abs(a, b):
    return abs(a - b)

#
# # 本地化时间
@register.filter
def local_datetime(_datetime):
    return filter_local_datetime(_datetime)


# 获取学生姓名，及详情链接
@register.filter
def get_name_detail(user, show_detail=True):
    user_name = get_user_name(user)
    if not show_detail:
        return user_name
    if settings.USER_DETAIL_EX_LINK:
        link = "<a href='" + settings.USER_DETAIL_EX_LINK + user.id.__str__() + "/'>" + user_name + "</a>"
    else:
        link = user_name
    return link