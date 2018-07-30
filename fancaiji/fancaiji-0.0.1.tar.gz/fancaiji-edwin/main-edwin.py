# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 10:00
# @Author  : yangyong
# @Email   : yangyong@findourlove.com
# @File    : demo.py
# @Software: PyCharm
# coding:utf-8
import json
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
from readability.readability import Document
from html.parser import HTMLParser
import urllib

url_page= sys.argv[1]
html = requests.get(url_page).content
title = Document(html).short_title()
content = HTMLParser().unescape(re.sub("</div></body></html>", '', re.sub("<html><body><div>", '', Document(html).summary()))).encode("utf-8")
data = json.dumps({"data":{"title":"{}".format(title),"content":"{}".format(content)}})
print(data)

