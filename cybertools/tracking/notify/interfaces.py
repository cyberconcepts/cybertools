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
Interface definitions for a notification framework.

$Id$
"""

from zope.interface import Interface, Attribute
from zope import schema

from cybertools.tracking.interfaces import ITrack


class INotificationManager(Interface):
    """ Provides methods for working with notifications.

        Typically used as an adapter for ITrackingStorage objects.
    """

    def notify(taskId, userName, type, media=None, **kw):
        """ Create a notification object according to the information given.
        """

    def cleanUp(age=1, removeIgnored=False):
        """ Remove old (finished) runs and (done) tracks; the last change
            (timeStamp) being before ``now - age`` days.

            If the ``removeIgnored`` argument is True remove also tracks
            in ``ignored`` state.
        """


class INotification(ITrack):
    """ A notification carries information necessary to inform a
        receiver (typically a user or person, but possibly also another
        kind of entity) about an event.
        The object the notification is related to is referenced via the
        task id attribute; interdependent notifications (i.e. notifications
        that are triggered by the identical event or have been created
        by another notification) share the run id; the user name references
        the user/person that will be notified.
    """

    type = Attribute('A string (token) that specifies the '
                'type of the notification.')
    state = Attribute('A string (token) specifying the '
                'current state of the notification.')
    priority = Attribute('A string (token) specifying the '
                'priority/importance of the notification.')
    parent = Attribute('The id of the parent notification, i.e. the '
                'notification that triggered the creation of this one. '
                'None if there is not parent notification.')
    eventType = Attribute('A string (token or title) that specifies the '
                'type of the event that triggered this notification.')
    media = Attribute('A collection of strings (tokens) specifying the '
                'media types that will be used for presenting '
                'the notification.')
    timingType = Attribute('A string (token) specifying the '
                'type of timing that will be used for presenting '
                'the notification.')
    timing = Attribute('A list of (typically) time/date values specifying '
                'the time range for presentation. The possible values and '
                'their interpretation depend on the timing type.')
    deliveryInfo = Attribute('Additional information needed for the '
                'delivery of the notification, e.g. an email address.')
    actionsPossible = Attribute('A collection of possible actions the receiver '
                'may take in response to the notification.')
    actionsTaken = Attribute('One or more actions that have been carried '
                'out in response to the notification.')

    # media + timingType + timing + deliveryInfo could be combined to
    # a `deliverySpec` attribute.

types = ('object_changed', 'object_new', 'invitation', 'assignment')
states = ('new', 'active', 'deferred', 'done', 'ignored')
priorities = ('critical', 'important', 'normal', 'info')
media = ('inbox', 'mail', 'im', 'rss')
timingTypes = ('immediate', 'hourly', 'daily', 'explicit')
actionTypes = ('accept', 'reject', 'ignore', 'note', 'delegate')

    # TODO: Action class (type + instance)
