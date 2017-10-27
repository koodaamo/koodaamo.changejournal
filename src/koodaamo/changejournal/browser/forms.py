import logging

from importlib import import_module

from z3c.form import form, field, button

from zope.component import getUtility
from zope.interface import providedBy, provider, Interface, implementer, invariant, Invalid
from zope.annotation.interfaces import IAnnotations
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope import schema

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


from plone import api
from plone.memoize import view as memoize

from plone.autoform import directives
from plone.supermodel import model

from ..interfaces import IChangeJournaled

from .. import _

logger = logging.getLogger("vidamin.plone.tablepage")


class ChangesReviewForm(form.Form):

   label = _(u"Purge journal")
   description = _(u"Purge the change journal, removing all entries.")

   ignoreContext=True

   template = ViewPageTemplateFile('templates/changes_review_template.pt')

   @button.buttonAndHandler(u'Purge')
   def handleApply(self, action):
      data, errors = self.extractData()
      if errors:
         self.status = self.formErrorsMessage
         return

      IChangeJournaled(self.context).clear()
      self.successMessage = u"Change journal cleared"
      self.status = self.successMessage
      return


   def journal(self):
      return tuple(IChangeJournaled(self.context).retrieve())
