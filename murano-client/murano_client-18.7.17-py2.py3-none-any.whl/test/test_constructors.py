import unittest
from murano_client.client import MuranoClient, MuranoClientException

class TestMuranoClient(unittest.TestCase):
    def test_no_kwargs(self):
        with self.assertRaises(MuranoClientException):
            MuranoClient()
    def test_no_watchlist(self):
        with self.assertRaises(MuranoClientException):
            MuranoClient(
                murano_host='mqtt://f5330e5s8cho0000.m2.exosite.io/')
    def test_good_mqtt_url(self):
        client = MuranoClient(
            watchlist=['config_io'],
            murano_host='mqtt://f5330e5s8cho0000.m2.exosite.io/'
        )
        self.assertEquals('mqtt', client.outbound_protocol)
    def test_good_http_url(self):
        client = MuranoClient(
            watchlist=['config_io'],
            murano_host='https://f5330e5s8cho0000.m2.exosite.io/'
        )
        self.assertEquals('https', client.outbound_protocol)

def main():
    unittest.main()

if __name__ == "__main__":
    main()