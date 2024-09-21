# cybertools.tracking.browser

""" View class(es) for tracking storage and tracks.
"""

from zope import component
from zope.browserpage import ViewPageTemplateFile
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
    def additionalMetadataFields(self):
        return [k for k in self.context.metadata.keys()
                  if k not in ('taskId', 'runId', 'userName', 'timeStamp')]

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

    def getMetadataTarget(self, key):
        value = self.metadata.get(key)
        return dict(title=value, url=None, obj=value)
