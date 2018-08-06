# -*- coding: utf-8 -*-

import logging
import unittest

from schleppy import transform

logging.basicConfig()
log = logging.getLogger('logger')
log.setLevel(logging.DEBUG)


class TestTransform(unittest.TestCase):

    def setUp(self):
        log.info("==================================================")
        log.info("======   Test: %s, SetUp", self.id())
        log.info("==================================================")

        self.source = {
            'address': {
                'one': '123 main street',
                'two': 'PO Box 1234'
            },
            'zip': {
                'code': 3321232,
                'province': None
            },
            'title': 'Warehouse',
            'state': 'CA'
        }

        self.sources_array = [{
            'address': {
                'one': '123 main street',
                'two': 'PO Box 1234'
            },
            'zip': {
                'code': 3321232,
                'province': None
            },
            'title': 'Warehouse',
            'state': 'CA'
        }, {
            'address': {
                'one': '456 market street',
                'two': 'PO Box 5678'
            },
            'zip': {
                'code': 9876,
                'province': None
            },
            'title': 'Garage',
            'state': 'NY'
        }]

    def tearDown(self):
        log.info("--------------------------------------------------")
        log.info("------   Test: %s, TearDown", self.id())
        log.info("--------------------------------------------------")

    def test_transforms_an_object_based_on_the_input_object(self):
        result = transform(self.source, {
            'person.address.lineOne': 'address.one',
            'person.address.lineTwo': 'address.two',
            'title': 'title',
            'person.address.region': 'state',
            'person.address.zip': 'zip.code',
            'person.address.location': 'zip.province'
        })

        expected = {
            "title": "Warehouse",
            "person": {
                "address": {
                    "lineTwo": "PO Box 1234",
                    "zip": 3321232,
                    "location": None,
                    "lineOne": "123 main street",
                    "region": "CA"
                }
            }
        }
        self.assertEqual(result, expected)

    def test_transforms_an_array_of_objects_based_on_the_input_object(self):
        result = transform(self.sources_array, {
            'person.address.lineOne': 'address.one',
            'person.address.lineTwo': 'address.two',
            'title': 'title',
            'person.address.region': 'state',
            'person.address.zip': 'zip.code',
            'person.address.location': 'zip.province'
        })

        expected = [
            {
                "person": {
                    "address": {
                        "lineOne": '123 main street',
                        "lineTwo": 'PO Box 1234',
                        "region": 'CA',
                        "zip": 3321232,
                        "location": None
                    }
                },
                "title": 'Warehouse'
            },
            {
                "person": {
                    "address": {
                        "lineOne": '456 market street',
                        "lineTwo": 'PO Box 5678',
                        "region": 'NY',
                        "zip": 9876,
                        "location": None
                    }
                },
                "title": 'Garage'
            }
        ]
        self.assertEqual(result, expected)

    def test_transforms_an_object_and_uses_the_reach_options_passed_into_it(self):
        result = transform(self.source, {
            'person-address-lineOne': 'address-one',
            'person-address-lineTwo': 'address-two',
            'title': 'title',
            'person-address-region': 'state',
            'person-prefix': 'person-title',
            'person-zip': 'zip-code'
        }, options={
            'separator': '-',
            'default': 'unknown'
        })

        expected = {
            "title": "Warehouse",
            "person": {
                "prefix": "unknown",
                "zip": 3321232,
                "address": {
                    "lineOne": "123 main street",
                    "lineTwo": "PO Box 1234",
                    "region": "CA"
                }
            }
        }
        self.assertEqual(result, expected)

    def test_uses_a_default_separator_for_keys_if_options_does_not_specify_on(self):
        result = transform(self.source, {
            'person.address.lineOne': 'address.one',
            'person.address.lineTwo': 'address.two',
            'title': 'title',
            'person.address.region': 'state',
            'person.prefix': 'person.title',
            'person.zip': 'zip.code'
        }, options={
            'default': 'unknown'
        })

        expected = {
            "title": "Warehouse",
            "person": {
                "prefix": "unknown",
                "zip": 3321232,
                "address": {
                    "lineOne": "123 main street",
                    "lineTwo": "PO Box 1234",
                    "region": "CA"
                }
            }
        }
        self.assertEqual(result, expected)

    def test_works_to_create_shallow_objects(self):
        result = transform(self.source, {
            'lineOne': 'address.one',
            'lineTwo': 'address.two',
            'title': 'title',
            'region': 'state',
            'province': 'zip.province'
        })

        expected = {
            "lineOne": '123 main street',
            "lineTwo": 'PO Box 1234',
            "title": 'Warehouse',
            "region": 'CA',
            "province": None
        }
        self.assertEqual(result, expected)

    def test_only_allows_strings_in_the_map(self):
        with self.assertRaises(ValueError):
            transform(self.source, {
                'lineOne': {}
            })

    def test_is_safe_to_pass_None(self):
        result = transform(None, {})

        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
