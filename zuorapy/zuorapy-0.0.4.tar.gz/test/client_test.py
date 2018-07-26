import unittest
import os

from zuorapy.client import Client
from consts import endpoint as ep, host as h


class ClientTest(unittest.TestCase):

    host = h.US_SANDBOX
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    def test_check_and_refresh_bearer_token(self):
        c = Client(host=self.host, client_id=self.client_id, client_secret=self.client_secret)

        self.assertIsNotNone(c.bearer_token, "Failed to retrieve bearer token!")

    def test_basic_get_200(self):
        endpoint = ep.CATALOG
        c = Client(host=self.host, username=self.username, password=self.password)
        res = c.get(endpoint=endpoint)

        self.assertEqual(res.status_code, 200, "GET request failure!")

    def test_basic_post_200(self):
        endpoint = ep.ACCOUNT_CRUD
        c = Client(host=self.host, username=self.username, password=self.password)
        payload = { "BillCycleDay": 1, "Currency": "USD", "Name": "Inki test account create from zuorapy", "Status": "Draft" }
        res = c.post(endpoint=endpoint, payload=payload)

        self.assertEqual(res.status_code, 200, "POST request failure!")

    def test_basic_put_200(self):
        test_acct_id = "2c92c0f964cff4f30164d3a831060c29"
        endpoint = "%s/%s" % (ep.ACCOUNT_CRUD, test_acct_id)
        c = Client(host=self.host, username=self.username, password=self.password)
        payload = { "Currency": "USD" }
        res = c.put(endpoint=endpoint, payload=payload)

        self.assertEqual(res.status_code, 200, "PUT request failure!")

    def test_basic_delete_200(self):
        test_acct_id = "2c92c0f9638c546c01638dc92fac138e"
        endpoint = "%s/%s" % (ep.ACCOUNT_CRUD, test_acct_id)
        c = Client(host=self.host, username=self.username, password=self.password)
        res = c.delete(endpoint=endpoint)

        self.assertEqual(res.status_code, 200, "DELETE request failure!")


if __name__ == '__main__':
    unittest.main()