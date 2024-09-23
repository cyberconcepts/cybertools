# cybertools.wiki.dcu.process

""" Node processor implementations for docutils nodes.
"""

from docutils.nodes import Text
from zope import component
from zope.cachedescriptors.property import Lazy
from zope.component import adapts

from cybertools.wiki.base.link import LinkProcessor
from cybertools.wiki.dcu.html import HTMLImageNode, HTMLReferenceNode
from cybertools.wiki.interfaces import IMediaManager


class Reference(LinkProcessor):

    adapts(HTMLReferenceNode)

    @Lazy
    def source(self):
        return self.context.document.context

    @Lazy
    def request(self):
        return self.context.document.request

    @Lazy
    def targetName(self):
        return self.context.node['refuri']

    def findTarget(self, manager, wiki, name):
        target = wiki.getPage(name)
        if target is None:
            return self.findTargetMedia(manager, wiki, name)
        return target

    def findTargetMedia(self, manager, wiki, name):
        mmName = wiki.getConfig('mediaManager')
        mm = component.getAdapter(wiki, IMediaManager, name=mmName)
        return mm.getObject(name)

    def setURI(self, uri):
        self.context.atts['href'] = uri

    def markPresentation(self, feature):
        self.context.atts['class'] += (' ' + feature)

    def addText(self, text):
        self.context.node.insert(0, Text(text))


class Image(Reference):

    adapts(HTMLImageNode)

    @Lazy
    def targetName(self):
        return self.context.node['uri']

    def findTarget(self, manager, wiki, name):
        return self.findTargetMedia(manager, wiki, name)

    def setURI(self, uri):
        self.context.atts['src'] = uri

    def markPresentation(self, feature):
        pass

