import unittest
import random
import toshare


class BaseEndpointTestCase(unittest.TestCase):
    random.seed()

    client = toshare