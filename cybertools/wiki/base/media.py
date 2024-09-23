# cybertools.wiki.base.media

""" Basic (sample) implementation for a wiki media manager and media objects.
"""

from zope.component import adapts
from zope.interface import implementer
from zope.traversing.browser import absoluteURL
from cybertools.wiki.interfaces import IWiki, IMediaManager, IMediaObject


@implementer(IMediaManager)
class WikiMediaManager(object):
    """ A Wiki adapter for providing media manager functionality. """

    adapts(IWiki)

    name = '.media'
    title = 'Wiki Media Manager'

    def __init__(self, context):
        self.context = context
        objects = getattr(context, '_media', None)
        if objects is None:
            objects = context._media = {}
        self.objects = objects

    def getWiki(self):
        return self.context

    def createObject(self, name, title=None):
        obj = MediaObject(name, title=title, parent=self.context)
        self.objects[name] = obj
        return obj

    def removeObject(self, name):
        del self.objects[name]

    def getObject(self, name):
        return self.objects.get(name)

    def listObjects(self):
        return self.objects.values()


@implementer(IMediaObject)
class MediaObject(object):
    """ A basic (maybe persistent) media object. """

    data = None

    def __init__(self, name, title=None, parent=None):
        self.name = name
        self.title = title or name
        self.parent = parent

    def getManager(self):
        if self.parent is None:
            return None
        mmName = self.parent.getConfig('mediaManager')
        return component.getAdapter(self.parent, IMediaManager, name=mmName)

    def getRawData(self):
        return self.data

    def setRawData(self, data):
        self.data = data

    # IWebResource

    @property
    def uid(self):
        return self.getUid()

    def getUid(self):
        return self.parent.getManager().getUid(self)
        #return self.getWiki().getManager().getUid(self)

    def getURI(self, request):
        return absoluteURL(self, request)

