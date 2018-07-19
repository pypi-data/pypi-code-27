import crayons
from django.test import Client, TestCase
from django.urls import reverse
from tokenservice.models import TokenApp

prefix = crayons.green('\noembedservice: ')
suffix = crayons.green(' ✓')


class TwitterTest(TestCase):
    def setUp(self):
        TokenApp.objects.create(app_name='test_app')

    def test_post(self):
        c = Client()
        url = reverse('oembedservice:twitter')
        test_app = TokenApp.objects.get(app_name='test_app')
        response = c.post(
            url,
            {
                "url": "https://twitter.com/jack/status/20"
            },
            HTTP_AUTHORIZATION='Token {}'.format(test_app.token)
        )

        print(prefix, 'Test twitter', suffix)
        self.assertEqual(response.status_code, 200)

        response = c.post(
            url,
            {
                "url": "https://twitter.com/jack/status/20",
                "maxwidth": 400
            },
            HTTP_AUTHORIZATION='Token {}'.format(test_app.token)
        )

        print(prefix, 'Test twitter with maxwidth', suffix)
        self.assertEqual(response.data.get('width'), 400)

        response = c.post(
            url,
            {
                "url": "https://twitter.com/jack/status/20",
                "omit_script": True
            },
            HTTP_AUTHORIZATION='Token {}'.format(test_app.token)
        )

        print(prefix, 'Test twitter without script', suffix)
        self.assertFalse('script' in response.data.get('html'))
