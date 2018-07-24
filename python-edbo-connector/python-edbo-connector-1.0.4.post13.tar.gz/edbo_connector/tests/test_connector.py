#!/usr/bin/python
# -*- coding: utf-8 -*-

from requests import Response
from ..connector import EDBOWebApiConnector


class TestEDBOWebApiConnector(object):
    def setup(self):
        self.connector = EDBOWebApiConnector()

    def test_execute(self):
        assert isinstance(self.connector.execute('auth/userInfo'), dict)
        assert isinstance(self.connector.execute('auth/userInfo', json_format=False), Response)
