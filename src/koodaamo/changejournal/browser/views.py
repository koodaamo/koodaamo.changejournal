from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations
from zope.publisher.interfaces import IPublishTraverse
from z3c.form import form, field, button
from zope.interface import provider, Interface, implementer, invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope import schema
from plone.supermodel import model

from .interfaces import IAccessTimestamped
from .. import TIMESTAMPS_KEY


@provider(IContextSourceBinder)
def get_keys(context):
   "provides timestamp key choice"

   try:
      keys = IAnnotations(context)[TIMESTAMPS_KEY].keys()
   except:
      keys = ()
   return SimpleVocabulary.fromValues(keys)

class ITimeStampResetting(model.Schema):
   "form schema"

   key = schema.Choice(
      source=get_keys,
      title=u"Key to reset",
      description=u"Choose key to reset",
      required=False,
   )
   all = schema.Bool(title=u"Reset all", description=u"Choose to reset all timestamps",
                     default=False)

   @invariant
   def eitherRequired(data):
      both = data.key and data.all
      neither = not (data.key or data.all)
      if both or neither:
         raise Invalid(_(u"Must either select a key or choose 'all'"))


@implementer(ITimeStampResetting)
class TimestampingReviewForm(form.Form):

   label = _(u"Reset timestamps")
   description = _(u"Reset a timestamp or all of them.")

   ignoreContext=True
   fields = field.Fields(ITimeStampResetting)

   template = ViewPageTemplateFile('timestamps.pt')

   @button.buttonAndHandler(u'Reset')
   def handleApply(self, action):
      data, errors = self.extractData()
      if errors:
         self.status = self.formErrorsMessage
         return

      try:
         timestamped = IAccessTimestamped(self.context)
      except:
         self.formErrorsMessage = u"Cannot access timestamps"
         return

      if data["all"] is True:
         timestamped.clear_all()
         self.successMessage = u"All timestamps cleared"
      else:
         timestamped.clear(data["key"])
         self.successMessage = u"Timestamp cleared"


   def timestamps(self):
      "get list of timestamps as (key, timestamp) tuples"

      try:
         timestamps = IAnnotations(self.context)[TIMESTAMPS_KEY]
      except:
         return None #raise Exception("cannot get timestamp annotations")
      else:
         return timestamps.items()



@implementer(IPublishTraverse)
class GetChanges(BrowserView):
   "return journal, as JSON or as HTML representation"

   html_changes_template = ViewPageTemplateFile("templates/html_changes_template.pt")

   def publishTraverse(self, request, key):
      "set key given as URL path parameter"
      self.timestampkey = key
      return self
