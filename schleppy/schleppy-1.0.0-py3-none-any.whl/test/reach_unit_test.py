# -*- coding: utf-8 -*-

import logging
import unittest

from schleppy import reach

logging.basicConfig()
log = logging.getLogger('logger')
log.setLevel(logging.DEBUG)


class TestReach(unittest.TestCase):

    def setUp(self):
        log.info("==================================================")
        log.info("======   Test: %s, SetUp", self.id())
        log.info("==================================================")

        self.obj = {
            'a': {
                'b': {
                    'c': {
                        'd': 1,
                        'e': 2
                    },
                    'f': 'hello'
                },
                'g': {
                    'h': 3
                }
            },
            'i': lambda: {},
            'j': None,
            'k': [4, 8, 9, 1]
        }

        self.obj['i'].x = 5

    def tearDown(self):
        log.info("--------------------------------------------------")
        log.info("------   Test: %s, TearDown", self.id())
        log.info("--------------------------------------------------")

    def test_returns_object_itself(self):
        self.assertEqual(reach(self.obj, None), self.obj)
        self.assertEqual(reach(self.obj, False), self.obj)
        self.assertEqual(reach(self.obj), self.obj)

    def test_returns_first_value_of_array(self):
        self.assertEqual(reach(self.obj, 'k.0'), 4)

    def test_returns_last_value_of_array_using_negative_index(self):
        self.assertEqual(reach(self.obj, 'k.-2'), 9)

    def test_returns_a_valid_member(self):
        self.assertEqual(reach(self.obj, 'a.b.c.d'), 1)

    def test_returns_a_valid_member_with_separator_override(self):
        self.assertEqual(reach(self.obj, 'a/b/c/d', options={'separator': '/'}), 1)

    def test_returns_none_from_none_object(self):
        self.assertEqual(reach(None, 'a.b.c.d'), None)

    def test_returns_none_from_missing_object_attribute(self):
        self.assertEqual(reach(self.obj, 'a.b.c.d.x'), None)

    def test_returns_none_from_missing_function_attribute(self):
        self.assertEqual(reach(self.obj, 'i.y'), None)

    def test_raises_keyerror_from_missing_object_attribute_in_strict_mode(self):
        with self.assertRaises(KeyError):
            reach(self.obj, 'a.b.c.o.x', options={'strict': True})

    def test_returns_none_from_invalid_attribute(self):
        self.assertEqual(reach(self.obj, 'a.b.c.d-.x'), None)

    def test_returns_function_property(self):
        self.assertEqual(reach(self.obj, 'i.x'), 5)

    def test_returns_none(self):
        self.assertEqual(reach(self.obj, 'j'), None)

    def test_returns_default_value(self):
        self.assertEqual(reach(self.obj, 'q', options={'default': 'testerino'}), 'testerino')

    def test_returns_nested_default_value(self):
        self.assertEqual(reach(self.obj, 'a.b.q', options={'default': 'testerino'}), 'testerino')


if __name__ == '__main__':
    unittest.main()
