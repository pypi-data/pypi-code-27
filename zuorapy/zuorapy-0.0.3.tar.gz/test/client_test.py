import unittest
import json

from zuorapy.client import Client
from consts import endpoint as ep, host as h


class ClientTest(unittest.TestCase):

    host = h.US_SANDBOX
    username = "ihong@zuora.com"
    password = "IH@t3MyL1f3"

    def test_get_200(self):
        endpoint = ep.CATALOG

        c = Client(host=self.host, username=self.username, password=self.password)

        res = c.get(endpoint=endpoint)

        self.assertEqual(res.status_code, 200, "GET request success!")

    # def test_post_200(self):


    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()