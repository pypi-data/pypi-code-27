# -*- coding: utf-8 -*-
from plone import api
from plone.oidc.testing import PLONE_OIDC_INTEGRATION_TESTING

import unittest


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class TestWorkflows(unittest.TestCase):
    """ """
    layer = PLONE_OIDC_INTEGRATION_TESTING

    def setUp(self):
        """ """
        self.portal = self.layer['portal']

    def test_oidc_default_user_workflows(self):
        """
        """
        workflow_tool = api.portal.get_tool('portal_workflow')

        self.assertIn('oidc_membrane_user_workflow', workflow_tool.getWorkflowIds())
        # xxx: more tests?

    def test_supports(self):
        """ """
        # Context mock
        workflow_tool = api.portal.get_tool('portal_workflow')
        # OidcTestUser content type bind with ``oidc_membrane_user_workflow`` workflow

        self.assertIn(
            'oidc_membrane_user_workflow',
            workflow_tool.getChainForPortalType('OidcTestUser')
        )
        # xxx: more tests?
