# -*- coding: utf-8 -*-

import unittest

from tapioca_trello import Trello


class TestTapiocaTrello(unittest.TestCase):

    def setUp(self):
        self.wrapper = Trello()


if __name__ == '__main__':
    unittest.main()
