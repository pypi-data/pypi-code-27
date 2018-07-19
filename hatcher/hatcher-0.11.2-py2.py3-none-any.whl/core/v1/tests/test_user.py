from hatcher.testing import unittest
from hatcher.core.tests.v1.base_test_user import BaseTestUser
from .user_responses import BroodResponses
from ..user import User


class TestUserV1(BaseTestUser, unittest.TestCase):

    def setUp(self):
        super(TestUserV1, self).setUp()
        self.user = User(
            'acme', 'user@acme.org', self.url_handler,
            model_registry=self.model_registry)
        self.brood_responses = BroodResponses(self.url_handler, self.user)
