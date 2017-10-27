from contextlib import contextmanager
from .interfaces import IAccessTimestamped
from .interfaces import IChangeJournaled


#
# context managers for timestamped journaling
#

@contextmanager
def timestamped_journal(key, obj):
   "get timestamped change journal for an object, with cleanup"

   timestamped = IAccessTimestamped(obj)
   journaled = IChangeJournaled(obj)

   # purge old journal entries
   journaled.clear(before=timestamped.oldest)

   # if this is first timestamped access, return journaled full contents, otherwise
   # return changes since last request
   if key not in timestamped:
      yield journaled.contentsjournal
   else:
      timestamp = timestamped.get(key) # latest timestamp for this key
      yield journaled.retrieve(since=timestamp) # changes since timestamp was last set

   # update timestamp
   if key:
      timestamped.update(key)


@contextmanager
def timestamped_journals(key, objs):
   "get timestamped change journal for objects, with cleanup"

   combined_journal = []
   for obj in objs:
      with timestamped_journal(key, obj) as journal:
         combined_journal.extend(journal)
   yield combined_journal

