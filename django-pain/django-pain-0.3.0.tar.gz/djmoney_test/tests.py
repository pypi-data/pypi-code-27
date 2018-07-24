from django.test import SimpleTestCase
from djmoney.money import Money

from djmoney_test.forms import MyModelForm
from djmoney_test.models import MyModel


class TestMyModelForm(SimpleTestCase):
    def setUp(self):
        self.instance = MyModel(amount=Money('42.00', 'USD'))

    def test_valid_form(self):
        form = MyModelForm(data={}, instance=self.instance)
        self.assertEqual(form.errors, {})
        self.assertTrue(form.is_valid())
