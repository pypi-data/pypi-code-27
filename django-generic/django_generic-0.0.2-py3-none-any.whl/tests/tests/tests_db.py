from django.test import TestCase

from django_generic.db import pks_from_iterable
from tests.factories import ExampleModelFactory
from tests.models import ExampleModel


class TestPksFromIterable(TestCase):
    def setUp(self):
        self.test_obj1 = ExampleModelFactory()
        self.test_obj2 = ExampleModelFactory()
        self.test_obj3 = ExampleModelFactory()
        self.queryset = ExampleModel.objects.all()
        self.list = [self.test_obj1, self.test_obj2.pk, self.test_obj3]
        self.tuple = (self.test_obj1, self.test_obj2.pk, self.test_obj3)
        self.set = set([self.test_obj1, self.test_obj2.pk, self.test_obj3])
        self.not_unique_list = [self.test_obj1, self.test_obj2.pk, self.test_obj1, self.test_obj3]

    def test_pks_from_iterable_use_queryset(self):
        pks = pks_from_iterable(self.queryset)
        self.assertEqual(len(pks), self.queryset.count())
        self.assertEqual(pks[0], self.queryset[0].pk)
        self.assertEqual(pks[1], self.queryset[1].pk)
        self.assertEqual(pks[2], self.queryset[2].pk)

    def test_pks_from_iterable_use_list(self):
        pks = pks_from_iterable(self.list)
        self.assertEqual(len(pks), len(self.list))
        self.assertEqual(pks[0], self.list[0].pk)
        self.assertEqual(pks[1], self.list[1])
        self.assertEqual(pks[2], self.list[2].pk)

    def test_pks_from_iterable_use_tuple(self):
        pks = pks_from_iterable(self.tuple)
        self.assertEqual(len(pks), len(self.tuple))
        self.assertEqual(pks[0], self.tuple[0].pk)
        self.assertEqual(pks[1], self.tuple[1])
        self.assertEqual(pks[2], self.tuple[2].pk)

    def test_pks_from_iterable_use_set(self):
        pks = pks_from_iterable(self.set)
        expected_data = [self.test_obj1.pk, self.test_obj2.pk, self.test_obj3.pk]
        self.assertEqual(len(pks), len(self.set))
        self.assertIn(pks[0], expected_data)
        self.assertIn(pks[1], expected_data)
        self.assertIn(pks[2], expected_data)

    def test_pks_from_iterable_use_else_format(self):
        self.assertRaises(TypeError, pks_from_iterable, ['another value', 12, self.test_obj1])
        self.assertRaises(TypeError, pks_from_iterable, [[1, 2, 3], 12, self.test_obj1])
        self.assertRaises(TypeError, pks_from_iterable, [{'ab': 12}, 12, self.test_obj1])

    def test_pks_from_iterable_with_unique(self):
        pks = pks_from_iterable(self.not_unique_list, unique_output=False)
        expected_data_without_unique = [self.test_obj1.pk, self.test_obj2.pk, self.test_obj1.pk, self.test_obj3.pk]
        self.assertEqual(pks[0], expected_data_without_unique[0])
        self.assertEqual(pks[1], expected_data_without_unique[1])
        self.assertEqual(pks[2], expected_data_without_unique[2])
        self.assertEqual(pks[3], expected_data_without_unique[3])

        pks = pks_from_iterable(self.not_unique_list, unique_output=True)
        expected_data_with_unique = [self.test_obj1.pk, self.test_obj2.pk, self.test_obj3.pk]
        self.assertEqual(len(pks), 3)
        self.assertEqual(pks[0], expected_data_with_unique[0])
        self.assertEqual(pks[1], expected_data_with_unique[1])
        self.assertEqual(pks[2], expected_data_with_unique[2])
