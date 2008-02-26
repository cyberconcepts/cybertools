#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Base classes for a notification framework.

$Id$
"""

from zope.component import adapts
from zope.interface import implements

from cybertools.tracking.btree import Track
from cybertools.tracking.interfaces import ITrackingStorage
from cybertools.tracking.notify.interfaces import INotification, INotificationManager


class NotificationManager(object):

    implements(INotificationManager)
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


class Notification(Track):

    implements(INotification)

    typeName = 'Notification'

    def __getattr__(self, attr):
        if attr in INotification:
            return self.data.get(attr)
        raise AttributeError(attr)

