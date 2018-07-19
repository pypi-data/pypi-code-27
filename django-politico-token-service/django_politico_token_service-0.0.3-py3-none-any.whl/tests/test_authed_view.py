import crayons
from django.test import Client, TestCase
from django.urls import reverse

from tokenservice.models import TokenApp

prefix = crayons.green('\ntokenservice: ')
suffix = crayons.green(' ✓')


class AuthTestViewTest(TestCase):
    def setUp(self):
        TokenApp.objects.create(app_name='test_app')

    def test_authorized(self):
        c = Client()
        url = reverse('tokenservice:test')
        test_app = TokenApp.objects.get(app_name='test_app')
        response = c.get(
            url,
            HTTP_AUTHORIZATION='Token {}'.format(test_app.token)
        )

        print(prefix, 'Test token-authorized GET view', suffix)
        self.assertEqual(response.status_code, 200)

        response = c.post(
            url,
            HTTP_AUTHORIZATION='Token {}'.format(test_app.token)
        )

        print(prefix, 'Test token-authorized POST view', suffix)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized(self):
        c = Client()
        url = reverse('tokenservice:test')
        test_app = TokenApp.objects.get(app_name='test_app')
        response = c.get(
            url,
            HTTP_AUTHORIZATION='Token {}XXX'.format(test_app.token)
        )

        print(prefix, 'Test bad token', suffix)
        self.assertEqual(response.status_code, 403)

        response = c.post(
            url,
        )

        print(prefix, 'Test missing token', suffix)
        self.assertEqual(response.status_code, 403)
