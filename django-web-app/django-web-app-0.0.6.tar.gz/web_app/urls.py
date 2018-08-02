# _*_ coding:utf-8 _*_
__author__ = 'WANGY'
__date__ = '2018/8/1 19:03'

from django.conf.urls import url, include

from .views.index import IndexView

urlpatterns = [
    url(r'^web/app/index/$', IndexView.as_view(), name="web_app_index"),
]