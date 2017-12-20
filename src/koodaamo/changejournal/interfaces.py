# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface, Attribute
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


class IKoodaamoChangejournalLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IAccessTimestamped(Interface):
   "timestamp annotator"

   def set(self, key):
      "set a timestamp"

   def get(self, key):
      "get the timestamp or None"


class IPortalAccessTimestamped(Interface):
   "marker"

class IChangeJournaled(Interface):
   "provide means to log changes to journal & get changes since timestamp"

   def log(operation, record):
      "log a new journal entry"

   def retrieve(since=None):
      "retrieve log entries since a given timestamp (as seconds since epoch)"


class IJournaledRecordGenerator(Interface):
   "iterable journaled record source"

   def __iter__(self):
      "must provide a record iterator"


class IPortalChangeJournaled(Interface):
   "marker for journaling content"


