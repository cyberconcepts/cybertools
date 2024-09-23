# cybertools.wiki.base.link

""" Basic (sample) implementations for links and link management.
"""

from docutils.nodes import Text
from zope.interface import implementer
from zope.traversing.browser import absoluteURL

from cybertools.link.interfaces import ILink, ILinkManager
from cybertools.wiki.interfaces import ILinkProcessor


@implementer(ILinkProcessor)
class LinkProcessor(object):
    """ Abstract base class. """

    source = request = None
    targetName = ''

    def __init__(self, context):
        self.context = context

    def process(self):
        if '..' in self.targetName:
            return
        wiki = self.source.getWiki()
        manager = wiki.getManager()
        lmName = self.source.getConfig('linkManager')
        lm = manager.getPlugin(ILinkManager, lmName)
        targetPageName = self.targetName
        params = fragment = ''
        if '?' in targetPageName:
            targetPageName, params = targetPageName.split('?', 1)
        if '#' in targetPageName:
            targetPageName, fragment = targetPageName.split('#', 1)
        #existing = iter(lm.query(source=self.source, name=self.targetName))
        for link in lm.query(source=self.source, name=self.targetName):
            #link = existing.next()
            if link.target is not None:
                target = self.getTarget(manager, wiki, link.target)
            else:
                target = None
            break
        else:
            target = self.findTarget(manager, wiki, targetPageName)
            link = lm.createLink(name=self.targetName,
                                 source=self.source, target=target)
        if fragment:
            link.targetFragment = fragment
        if params:
            link.targetParameters = params
        if self.request is not None:
            if target is None:
                #uri = link.refuri = '%s/create.html?name=%s' % (
                uri = '%s/@@create.html?name=%s' % (
                                absoluteURL(wiki, self.request), link.name)
            else:
                uri = target.getURI(self.request)
                uri += self.fragmentAndParams(fragment, params)
        self.setURI(uri)
        if target is None:
            self.markPresentation('create')
            self.addText('?')

    def findTarget(self, manager, wiki, name):
        return wiki.getPage(name)

    def getTarget(self, manager, wiki, uid):
        return manager.getObject(uid)

    def fragmentAndParams(self, fragment, params):
        f = p = ''
        if fragment:
            f = '#' + fragment
        if params:
            p = '?' + params
        return f + p

    def setURI(self, uri):
        raise ValueError('To be implemented by subclass.')

    def markPresentation(self, feature):
        raise ValueError('To be implemented by subclass.')

    def addText(self, text):
        raise ValueError('To be implemented by subclass.')

