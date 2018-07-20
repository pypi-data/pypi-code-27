# -*- coding: utf-8 -*-
from plone import api
from plone.behavior.interfaces import IBehavior
from plone.dexterity.behavior import DexterityBehaviorAssignable
from plone.oidc.membrane.behaviors import IOidConnectClaims
from plone.oidc.testing import PLONE_OIDC_INTEGRATION_TESTING
from zope.component import queryUtility

import unittest


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class TestBehaviors(unittest.TestCase):
    """ """
    layer = PLONE_OIDC_INTEGRATION_TESTING

    def setUp(self):
        """ """
        self.portal = self.layer['portal']

    def test_defined_behaviors(self):
        """Auto Behavior Name::

            >>> from plone.oidc.membrane.behaviors import IOidConnectClaims
            >>> print IOidConnectClaims.__identifier__
            fhir.heart.behavior.user.IOidConnectClaims
        """
        oid_connection_claims = queryUtility(IBehavior, name='plone.oidc.membrane.behaviors.IOidConnectClaims')
        self.assertIsNotNone(oid_connection_claims)

    def test_supports(self):
        """ """
        # Context mock
        with api.env.adopt_roles('Manager'):
            id_ = self.portal.invokeFactory('OidcTestUser', 'test_oidc_user')  # noqa: P001
            user_context = self.portal[id_]

        # Test: OidcTestUser has expected behaviors
        assignable = DexterityBehaviorAssignable(user_context)
        self.assertEqual(True, assignable.supports(IOidConnectClaims))

    def test_enumerate(self):
        """ """
        with api.env.adopt_roles('Manager'):
            id_ = self.portal.invokeFactory('OidcTestUser', 'test_oidc_user2')  # noqa: P001
            user_context = self.portal[id_]

        oid_connection_claims = queryUtility(IBehavior, name=IOidConnectClaims.__identifier__)

        assignable = DexterityBehaviorAssignable(user_context)
        self.assertIn(
            oid_connection_claims,
            list(assignable.enumerateBehaviors())
        )
