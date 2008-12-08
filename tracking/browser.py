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
View class(es) for tracking storage and tracks.

$Id$
"""

from zope import component
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope.security.proxy import removeSecurityProxy
from zope.traversing.api import getName
from zope.traversing.browser import absoluteURL

from cybertools.container.base import ContainerView, contents_template
from cybertools.tracking.btree import timeStamp2ISO


tracks_template = ViewPageTemplateFile('tracks.pt')
track_template = ViewPageTemplateFile('track.pt')


class TrackingStorageView(ContainerView):

    contents_template = contents_template
    template = tracks_template

    def __call__(self):
        return self.template()

    def getTracks(self):
        for tr in reversed(removeSecurityProxy(self.context.values())):
            view = component.queryMultiAdapter((tr, self.request), name='index.html')
            if view:
                yield view
            else:
                yield TrackView(tr, self.request)


class TrackView(object):

    template = track_template

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return self.template()

    @Lazy
    def id(self):
        return getName(self.context)

    @Lazy
    def url(self):
        return absoluteURL(self.context, self.request)

    @Lazy
    def metadata(self):
        return self.context.metadata

    @Lazy
    def task(self):
        return self.metadata['taskId']

    taskTitle = task
    taskUrl = None

    @Lazy
    def run(self):
        return self.metadata['runId']

    @Lazy
    def user(self):
        return self.metadata['userName']

    userTitle = user
    userUrl = None

    @Lazy
    def timeStamp(self):
        return timeStamp2ISO(self.metadata['timeStamp'])
