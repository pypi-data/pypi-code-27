# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class PloneOidcLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        z2.installProduct(app, 'Products.membrane')

        import plone.restapi
        self.loadZCML(package=plone.restapi)

        import Products.membrane
        self.loadZCML(package=Products.membrane)

        import dexterity.membrane
        self.loadZCML(package=dexterity.membrane)

        import plone.oidc
        self.loadZCML(package=plone.oidc)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.membrane:default')
        applyProfile(portal, 'dexterity.membrane:default')
        applyProfile(portal, 'plone.restapi:default')
        applyProfile(portal, 'plone.oidc:default')
        applyProfile(portal, 'plone.oidc:testing')


PLONE_OIDC_FIXTURE = PloneOidcLayer()


PLONE_OIDC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_OIDC_FIXTURE,),
    name='PloneOidcLayer:IntegrationTesting',
)


PLONE_OIDC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_OIDC_FIXTURE,),
    name='PloneOidcLayer:FunctionalTesting',
)


PLONE_OIDC_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONE_OIDC_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='PloneOidcLayer:AcceptanceTesting',
)
