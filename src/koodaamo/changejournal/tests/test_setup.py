# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from koodaamo.changejournal.testing import KOODAAMO_CHANGEJOURNAL_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that koodaamo.changejournal is properly installed."""

    layer = KOODAAMO_CHANGEJOURNAL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if koodaamo.changejournal is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'koodaamo.changejournal'))

    def test_browserlayer(self):
        """Test that IKoodaamoChangejournalLayer is registered."""
        from koodaamo.changejournal.interfaces import (
            IKoodaamoChangejournalLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IKoodaamoChangejournalLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = KOODAAMO_CHANGEJOURNAL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['koodaamo.changejournal'])

    def test_product_uninstalled(self):
        """Test if koodaamo.changejournal is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'koodaamo.changejournal'))

    def test_browserlayer_removed(self):
        """Test that IKoodaamoChangejournalLayer is removed."""
        from koodaamo.changejournal.interfaces import \
            IKoodaamoChangejournalLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           IKoodaamoChangejournalLayer,
           utils.registered_layers())
