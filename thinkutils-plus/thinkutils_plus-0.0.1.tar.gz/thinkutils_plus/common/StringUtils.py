#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

def is_empty_string(szStr):
    try:
        if szStr is None or 0 == len(szStr.strip()):
            return True
        else:
            return False
    except Exception as e:
        return True


# print is_empty_string(180)
# print is_empty_string("180")