# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import koodaamo.changejournal


class KoodaamoChangejournalLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=koodaamo.changejournal)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'koodaamo.changejournal:default')


KOODAAMO_CHANGEJOURNAL_FIXTURE = KoodaamoChangejournalLayer()


KOODAAMO_CHANGEJOURNAL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(KOODAAMO_CHANGEJOURNAL_FIXTURE,),
    name='KoodaamoChangejournalLayer:IntegrationTesting'
)


KOODAAMO_CHANGEJOURNAL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(KOODAAMO_CHANGEJOURNAL_FIXTURE,),
    name='KoodaamoChangejournalLayer:FunctionalTesting'
)


KOODAAMO_CHANGEJOURNAL_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        KOODAAMO_CHANGEJOURNAL_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='KoodaamoChangejournalLayer:AcceptanceTesting'
)
