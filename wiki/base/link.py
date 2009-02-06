#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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
Basic (sample) implementations for links and link management

$Id$
"""

from docutils.nodes import Text
from zope.interface import implements
from zope.traversing.browser import absoluteURL

from cybertools.wiki.interfaces import ILink, ILinkManager, ILinkProcessor


class LinkManager(object):
    """ A very basic link manager implementation.
    """

    implements(ILinkManager)

    def __init__(self):
        self.links = {}
        self.linksBySource = {}

    def createLink(self, name, source, target, **kw):
        link = Link(name, source, target, **kw)
        link.manager = self
        id = self.generateLinkIdentifier(link)
        self.links[id] = link
        self.linksBySource.setdefault(source, []).append(link)
        return link

    def removeLink(self, link):
        if link.identifier in self.links:
            link.manager = None
            del self.links[link.identifier]

    def query(self, source=None, target=None, name=None, **kw):
        if source is None:
            result = self.links.values()
        else:
            result = self.linksBySource.get(source, [])
        kw.update(dict(target=target, name=name))
        for k, v in kw.items():
            if v is None:
                continue
            if not isinstance(v, (list, tuple)):
                v = [v]
            result = [r for r in result if getattr(r, k) in v]
        return result

    def generateLinkIdentifier(self, link):
        identifier = '%07i' % (max([int(k) for k in self.links.keys()] or [0]) + 1)
        link.identifier = identifier
        return identifier


class Link(object):

    implements(ILink)

    identifier = None
    manager = None

    def __init__(self, name, source, target, **kw):
        self.name = name
        self.source = source
        self.target = target
        for k, v in kw.items():
            if k not in ILink:
                raise AttributeError(k)
            setattr(self, k, v)

    def getManager(self):
        return self.manager

    def __getattr__(self, attr):
        if attr not in ILink:
            raise AttributeError(attr)
        return self.__dict__.get(attr)


class LinkProcessor(object):
    """ Abstract base class. """

    implements(ILinkProcessor)

    source = request = None
    targetName = ''

    def __init__(self, context):
        self.context = context

    def process(self):
        wiki = self.source.getWiki()
        manager = wiki.getManager()
        sourceUid = manager.getUid(self.source)
        lmName = self.source.getConfig('linkManager')
        lm = wiki.getManager().getPlugin(ILinkManager, lmName)
        existing = lm.query(source=sourceUid, name=self.targetName)
        if existing:
            link = list(existing)[0]
            target = manager.getObject(link.target)
        else:
            target = wiki.getPage(self.targetName)
            targetUid = manager.getUid(target)
            link = lm.createLink(self.targetName, sourceUid, targetUid)
        if link.refuri is None:
            if self.request is not None:
                if target is None:
                    link.refuri = '%s/create.html?linkid=%s' % (
                                    absoluteURL(wiki, self.request), link.identifier)
                else:
                    link.refuri = absoluteURL(target, self.request)
        self.setURI(link.refuri)
        if target is None:
            self.markPresentation('create')
            self.addText('?')

    def setURI(self, uri):
        raise ValueError('To be implemented by subclass.')

    def markPresentation(self, feature):
        raise ValueError('To be implemented by subclass.')

    def addText(self, text):
        raise ValueError('To be implemented by subclass.')
