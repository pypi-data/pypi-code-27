from django.contrib.auth.models import User
from django.test import TestCase


class TestLogin(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="ozcan", password="pass12345")
        self.superuser = User.objects.create_superuser(username="super", password="pass12345", email="super@mail.com")

    def test_user(self):
        user = User.objects.get(username="ozcan")
        self.assertEqual(self.user, user)

    def test_superuser(self):
        superuser = User.objects.get(username="super")
        self.assertEqual(self.superuser, superuser)

    def test_is_not_superuser(self):
        user = User.objects.filter(is_superuser=False).get(username="ozcan")
        self.assertEqual(self.user, user)

    def test_is_superuser(self):
        superuser = User.objects.filter(is_superuser=True).get(username="super")
        self.assertEqual(self.superuser, superuser)

    def test_user_login(self):
        user = self.client.login(username="ozcan", password="pass12345")
        self.assertTrue(user)

    def test_superuser_login(self):
        superuser = self.client.login(username="super", password="pass12345")
        self.assertTrue(superuser)

    def test_login_status_code(self):
        response = self.client.post("/authen/login/", data={"username": "super", "password": "pass12345"})
        self.assertEqual(response.status_code, 200)

    def test_login_response_valid(self):
        response = self.client.post("/authen/login/", data={"username": "super", "password": "pass12345"})
        self.assertEqual(response.json(), {'isValid': True, 'payload': 'super'})

    def test_login_response_invalid(self):
        response = self.client.post("/authen/login/", data={"username": "ozcan", "password": "wrong"})
        self.assertEqual(response.json(), {'isValid': False, 'payload': '<strong>Invalid credentials</strong>'})

    def test_logout(self):
        response = self.client.logout()
        self.assertIsNone(response)
