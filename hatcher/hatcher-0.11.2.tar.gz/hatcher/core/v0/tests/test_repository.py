from hatcher.testing import unittest
from hatcher.core.tests.v0.base_test_repository import BaseTestRepository
from .repository_responses import BroodResponses
from ..repository import Repository


class TestRepositoryV0(BaseTestRepository, unittest.TestCase):

    def setUp(self):
        super(TestRepositoryV0, self).setUp()
        self.repository = Repository(
            'enthought', 'free', self.url_handler,
            model_registry=self.model_registry)
        self.brood_responses = BroodResponses(
            self.url_handler, self.repository)
