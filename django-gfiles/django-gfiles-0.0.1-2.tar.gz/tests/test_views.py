# -*- coding: utf-8 -*-
#  python manage.py test misa -v 3 --keepdb
#  coverage run --source='.' manage.py test galaxy -v 3 --keepdb
#  coverage report
#  coverage html --omit="admin.py"
from __future__ import unicode_literals, print_function

import os
from django.core.files import File
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from gfiles.views import GFileCreateView, GFileListView
from gfiles.models import GenericFile

def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request

def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_response(request)
    return request


class UserAccountTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')

    def test_signup(self):
        print(reverse('register'))

        response = self.client.post('/register/', {
            'username': 'admin99',
            'password1': 'qwertyui',
            'password2': 'qwertyui',
            'email': 'admin@example.com'})

        print(User.objects.all())
        print(response.status_code)
        print(response)
        user = User.objects.get(username="admin99")
        self.assertEqual(user.username, "admin99")
        self.assertEqual(response.status_code, 302)  # if it's successful it redirect


class GFileCreateViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')

        self.test_data_file_pth = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tests', 'data',
                                          'test_data_file.tsv')

    def test_login_redirect(self):
        """
        Test to check if a guest user is redirect to the login page
        """
        request = self.factory.get(reverse('upload_gfile'))

        print(self.user)
        request.user = AnonymousUser()
        request = add_middleware_to_request(request, SessionMiddleware)
        response = GFileCreateView.as_view()(request)
        # print(response)

        # client acts as a fake website for the request
        response.client = Client()

        self.assertRedirects(response, '/login/?next=/upload_gfile/')

    def test_get(self):
        """
        """
        request = self.factory.get(reverse('upload_gfile'))
        request.user = self.user
        response = GFileCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)  # done without error

    def test_post_valid_url(self):
        """
        Test post with valid url
        """
        gfile_before = len(GenericFile.objects.all())

        with open(self.test_data_file_pth) as fp:
            self.client.force_login(self.user)
            response = self.client.post(reverse('upload_gfile'),
                                    {'data_file': fp})
            self.assertEqual(response.status_code, 302)  # redirected page (e.g. success page)
            print(GenericFile.objects.all())
            self.assertEqual(len(GenericFile.objects.all()), gfile_before + 1)



class GFileListViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        self.test_data_file_pth = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                               'tests', 'data', 'test_data_file.tsv')
        self.gfile = GenericFile(original_filename='test_data_file.tsv', user=self.user)
        self.gfile.data_file.save('test_data_file.tsv', File(open(self.test_data_file_pth, 'r')))

    def test_get_anom(self):
        """
        Any user should be able to see the table
        """
        request = self.factory.get(reverse('gfile_summary'))

        print(self.user)
        request.user = AnonymousUser()
        request = add_middleware_to_request(request, SessionMiddleware)
        response = GFileListView.as_view()(request)
        # print(response)

        # client acts as a fake website for the request
        response.client = Client()

        self.assertEqual(response.status_code, 200)  # done without error

    def test_get_table_entry(self):
        """
        Check elements in table
        """
        request = self.factory.get(reverse('gfile_summary'))

        print(self.user)
        request.user = AnonymousUser()
        request = add_middleware_to_request(request, SessionMiddleware)
        response = GFileListView.as_view()(request)
        # print(response)

        # client acts as a fake website for the request
        response.client = Client()

        self.gfile = GenericFile(original_filename='test_data_file.tsv', user=self.user)
        self.gfile.data_file.save('test_data_file.tsv', File(open(self.test_data_file_pth, 'r')))


        self.assertContains(response, '<div class="table-container">')
        self.assertContains(response, '<div id="GFileTableWithCheck" class="column-shifter-container">')
        self.assertContains(response, '<table  class="paleblue">')
        self.assertContains(response, '<td class="filename">test_data_file.tsv</td>')

