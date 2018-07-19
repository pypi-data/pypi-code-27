import crayons
from django.test import Client, TestCase
from django.urls import reverse
from tokenservice.models import TokenApp

prefix = crayons.green('\noembedservice: ')
suffix = crayons.green(' ✓')


class YouTubeTest(TestCase):
    def setUp(self):
        TokenApp.objects.create(app_name='test_app')

    def test_post(self):
        c = Client()
        url = reverse('oembedservice:youtube')
        test_app = TokenApp.objects.get(app_name='test_app')
        response = c.post(
            url,
            {
                "url": "https://www.youtube.com/watch?v=V7uEb_XrK1U"
            },
            HTTP_AUTHORIZATION='Token {}'.format(test_app.token)
        )

        print(prefix, 'Test YouTube', suffix)
        self.assertEqual(response.status_code, 200)
