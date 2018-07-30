#!/usr/bin/env python

import json
import unittest
from vmwvro2.sessions import Session, SessionList




class Test_Session(unittest.TestCase):


    #####################
    def test_basic_sesion(self):

        login = 'login'
        password = 'password'
        proxies = dict(https='socks5://127.0.0.1:8888')


        s1 =    Session(alias="dev-de", 
                        url="host", 
                        username=login, 
                        password=password,
                        proxies=proxies,
                        tags=['dev', 'rat'])

        self.assertIsNotNone(s1)
        self.assertEqual(s1.username, "login")
        self.assertIsNotNone(s1.basic_auth)
        self.assertEqual(s1.url, "https://host:8281")
        self.assertTrue('dev' in s1.tags)


    #####################
    def test_sesion_list(self):
        sl = SessionList()
        sl.load()
        self.assertIsNotNone(sl)

        s1 =sl.list['dev-de']
        self.assertIsNotNone(s1)
        self.assertRegexpMatches(s1.url, r'^https://cide.*:8281$')
        self.assertRegexpMatches(s1.username, r'^vf.*@.*com$')





if __name__ == '__main__':
    unittest.main()
