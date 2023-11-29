# cybertools.tracking.notify.base

"""Base classes for a notification framework.
"""

from zope.component import adapts
from zope.interface import implementer

from cybertools.tracking.btree import Track
from cybertools.tracking.interfaces import ITrackingStorage
from cybertools.tracking.notify.interfaces import INotification, INotificationManager


@implementer(INotificationManager)
class NotificationManager(object):

    adapts(ITrackingStorage)

    def __init__(self, context):
        self.context = context

    def notify(self, taskId, userName, ntfType, media=None, priority='info', **kw):
        runId = self.context.startRun()
        if media is None:
            media = ['inbox']
        data = dict(type=ntfType, state='new', media=media)
        data.update(kw)
        self.context.saveUserTrack(taskId, runId, userName, data)

    def cleanUp(self, age=1, removeIgnored=False):
        pass

    def query(self, **kw):
        return self.context.query(**kw)


@implementer(INotification)
class Notification(Track):

    typeName = 'Notification'

    def __getattr__(self, attr):
        if attr in INotification:
            return self.data.get(attr)
        raise AttributeError(attr)

