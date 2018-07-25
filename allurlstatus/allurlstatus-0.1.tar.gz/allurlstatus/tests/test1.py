from unittest import TestCase

import allurlstatus


class TestUrls(TestCase):
    def test_is_string(self):
        s = allurlstatus.data
        self.assertTrue(isinstance(s, list))
