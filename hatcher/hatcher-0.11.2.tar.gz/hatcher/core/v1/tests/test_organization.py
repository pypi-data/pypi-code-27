from hatcher.testing import unittest
from hatcher.core.tests.v1.base_test_organization import BaseTestOrganization
from .organization_responses import BroodResponses
from ..organization import Organization
from ..repository import Repository
from ..user import User


class TestOrganizationV1(BaseTestOrganization, unittest.TestCase):

    def setUp(self):
        super(TestOrganizationV1, self).setUp()
        self.user_type = User
        self.repository_type = Repository
        self.organization = Organization(
            'acme', url_handler=self.url_handler,
            model_registry=self.model_registry)
        self.brood_responses = BroodResponses(self.url_handler)
