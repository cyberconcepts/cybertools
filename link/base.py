#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
A simple generic, general-purpose link management framework.

$Id$
"""

from BTrees.IFBTree import intersection, union
from BTrees.IOBTree import IOBTree
from persistent import Persistent
from zope import component
from zope.component import adapts
from zope.index.field import FieldIndex
from zope.interface import implements
from zope.app.intid.interfaces import IIntIds

from cybertools.link.interfaces import ILinkManager, ILink


class LinkManager(Persistent):
    """ A manager (storage, registry) for link objects.
    """

    implements(ILinkManager)

    uid = int

    # initialization

    def __init__(self):
        self.links = IOBTree()
        self.setupIndexes()
        self.currentId = 0

    def setupIndexes(self):
        self.indexes = dict(
                name=FieldIndex(),
                source=FieldIndex(),
                target=FieldIndex())

    # public methods

    def createLink(self, **kw):
        if not 'name' in kw or not 'source' in kw:
            raise ValueError("At least 'name' and 'source' attributes must "
                             "be given.")
        identifier = self.generateIdentifier()
        link = Link(self, identifier)
        link.update(**kw)
        self.getLinks()[identifier] = link
        self.indexLink(link)
        return link

    def removeLink(self, link):
        del self.getLinks()[link.identifier]

    def getLink(self, identifier):
        return self.getLinks()[identifier]

    def query(self, name=None, source=None, target=None, **kw):
        source = self.getUniqueId(source)
        target = self.getUniqueId(target)
        r = None
        if name is not None:
            r = self.indexes['name'].apply((name, name))
        if source is not None:
            r = self.intersect(r, self.indexes['source'].apply((source, source)))
        if target is not None:
            r = self.intersect(r, self.indexes['target'].apply((target, target)))
        if r is None:
            raise ValueError("At least one critera of 'name', 'source', or "
                             "'target' must be given.")
        result = [self.getLink(id) for id in r]
        #for k, v in kw:
        #    result = [link for link in result if getattr(link, k) == v]
        return sorted(result, key=lambda x: (x.order, x.name))

    def __iter__(self):
        return self.getLinks().values()

    # protected methods

    def getLinks(self):
        return self.links

    def generateIdentifier(self):
        self.currentId += 1
        return self.currentId

    def indexLink(self, link):
        for attr, idx in self.indexes.items():
            value = getattr(link, attr)
            if value is None:
                idx.unindex_doc(link.identifier)
            else:
                idx.index_doc(link.identifier, value)

    def intersect(self, r1, r2):
        return r1 is None and r2 or intersection(r1, r2)

    def getUniqueId(self, obj):
        if obj is None:
            return None
        if isinstance(obj, self.uid):
            return obj
        # TODO: take external objects (referenced by URIs) in to account
        return component.getUtility(IIntIds).getId(obj)

    def getObject(self, uid):
        return component.getUtility(IIntIds).getObject(uid)


class Link(Persistent):
    """ A basic link implementation.
    """

    implements(ILink)

    defaults = dict(target=None,
                    linkType=u'link',
                    state=u'valid',
                    relevance=1.0,
                    order=0,)

    def __init__(self, manager, identifier):
        self.manager = self.__parent__ = manager
        self.identifier = self.__name__ = identifier

    def getManager(self):
        return self.manager

    def getSource(self):
        return self.getManager().getObject(self.source)

    def getTarget(self):
        return self.getManager().getObject(self.target)

    def update(self, **kw):
        manager = self.getManager()
        for k in ('source', 'target'):
            if k in kw:
                kw[k] = manager.getUniqueId(kw[k])
        for k, v in kw.items():
            setattr(self, k, v)
        for k in manager.indexes:
            if k in kw:
                manager.indexLink(self)
                break

    def __getattr__(self, attr):
        if attr not in ILink:
            raise AttributeError(attr)
        value = self.defaults.get(attr, u'')
        return value
