import time
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.interface import implementer
from zope.annotation.interfaces import IAnnotations

from .interfaces import IAccessTimestamped
from .interfaces import IChangeJournaled
from .interfaces import IJournaledRecordGenerator

from . import TIMESTAMPS_KEY


@implementer(IAccessTimestamped)
class AccessTimeStamped(object):
   "timestamp annotator"

   def __init__(self, context):
      self.context = context

   @property
   def timestamps(self):
      annotations = IAnnotations(self.context)
      try:
         return annotations[TIMESTAMPS_KEY]
      except:
         annotations[TIMESTAMPS_KEY] = PersistentDict()
         return annotations[TIMESTAMPS_KEY]

   def __contains__(self, key):
      "check if we have a timestamp for key"
      return True if key in self.timestamps.keys() else False

   def set(self, key, timestamp):
      "set a timestamp"
      self.timestamps[key] = timestamp

   def update(self, key):
      "set timestamp to current time"
      self.set(key, time.time())

   def get(self, key):
      "get the timestamp or None"
      return self.timestamps.get(key)

   @property
   def oldest(self):
      "get oldest timestamp"
      stamps = self.timestamps.values()
      return min(stamps) if stamps else 0

   def clear(self, key):
      "remove a timestamp"
      del self.timestamps[key]

   def clear_all(self):
      "remove all timestamps"
      self.timestamps.clear()



@implementer(IChangeJournaled)
class ChangeJournaled(object):
   "keep a timestamped journal of changes; meant for fairly short change tracks"

   JOURNAL_KEY = "record_change_journal"

   REMOVE = -1
   CHANGE = 0
   ADD = 1

   def __init__(self, context):
      self.context = context

   @property
   def _journal(self):
      annotations = IAnnotations(self.context)
      try:
         return annotations[self.JOURNAL_KEY]
      except:
         annotations[self.JOURNAL_KEY] = PersistentList()
         return annotations[self.JOURNAL_KEY]

   @property
   def contentsjournal(self):
      "produce a journal of current contents"
      ts = time.time()
      return [(ts, 1, record) for record in IJournaledRecordGenerator(self.context)]

   def log(self, operation, record):
      "make a new journal entry"

      # TODO: to log changes, perhaps just store full old version if there is no reference
      # to the old version in the journal, likewise for removals; store full removed if
      # there is no reference earlier (reference by __uuid__)?

      if operation in (self.ADD, self.REMOVE, self.CHANGE):
         entry = (time.time(), operation, record)
         self._journal.append(entry)
      else:
         raise Exception("Unknown operation, use ADD/CHANGE/REMOVE ie. 1/0/-1")

   def clear(self, before=None):
      "empty the journal, optionally before a given timestamp (seconds after epoch)"

      if before is None:
         cleaned_count = len(self._journal)
         del self._journal[:]
      else:
         old_entries = [e for e in self._journal if e[0] < before]
         cleaned_count = len(old_entries)
         for entry in old_entries:
            self._journal.remove(entry)
      return cleaned_count


   def retrieve(self, since=0):
      "retrieve log entries since a given timestamp (seconds after epoch)"

      return (e for e in self._journal if e[0] >= since)
