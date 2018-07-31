#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import json

class BaseObject(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return json.loads(self.to_json())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def format(self):
        return self.to_dict()

    def __str__(self):
        return self.to_json()
