import unittest

from pyojm.models import Model
from pyojm.attributes import *


class TestJsonModel(unittest.TestCase):
    def test_positive_01(self):

        data = {
            'string_a': 'foo',
            'string_list_a': ['foo', 'bar'],
            'number_a': 1,
            'number_list_a': [1, 2],
            'boolean_a': True,
            'boolean_list_a': [True, False],
            'list_a': ['foo', 1],
            'object_a': {
                'foo': 'bar'
            }
        }

        class TestModel(Model):
            class Meta:
                strict_validation = True
            string_a = StringAttribute('string_a')
            string_list_a = StringListAttribute('string_list_a.[*]')
            number_a = NumberAttribute('number_a')
            number_list_a = NumberListAttribute('number_list_a.[*]')
            boolean_a = BooleanAttribute('boolean_a')
            boolean_list_a = BooleanListAttribute('boolean_list_a.[*]')
            list_a = ListAttribute('list_a.[*]')
            object_a = ObjectAttribute('object_a')

        t = TestModel(data)

        self.assertEqual('foo', t.string_a)
        self.assertEqual(['foo', 'bar'], t.string_list_a)
        self.assertEqual(1, t.number_a)
        self.assertEqual([1, 2], t.number_list_a)
        self.assertEqual(True, t.boolean_a)
        self.assertEqual([True, False], t.boolean_list_a)
        self.assertEqual(['foo', 1], t.list_a)
        self.assertEqual({
            'foo': 'bar'
        }, t.object_a)

    def test_negative_01(self):
        data = {
            'string_a': 1
        }

        class TestModel(Model):
            class Meta:
                strict_validation = True
            string_a = StringAttribute('string_a')

        t = TestModel(data)
        with self.assertRaises(TypeError):
            print(t.string_a)
