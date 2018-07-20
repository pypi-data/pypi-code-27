# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 11:30
# @Author  : LI Jiawei
# @Email   : jliea@connect.ust.hk
# @File    : nszbd.py
# @Software: PyCharm

import time
import os

words = "Ti Amo je t'aime ich liebe dich σε αγαπώ se agapo"
for item in words.split():
    print('\n'.join([''.join([(item[(x-y) % len(item)] if ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(12, -12, -1)]))
    time.sleep(1.5)
    os.system("cls")