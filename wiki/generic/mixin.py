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
Wiki implementation = mixin classes for Zope2 content objects.

$Id$
"""

from BTrees.IOBTree import IOTreeSet
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.cachedescriptors.property import Lazy
from zope import component
from zope.component import adapts
from zope.interface import implements

from cybertools.link.base import Link, LinkManager as BaseLinkManager
from cybertools.link.interfaces import ILinkManager
from cybertools.util.generic.interfaces import IGenericObject, IGenericFolder
from cybertools.wiki.base.config import WikiConfigInfo, BaseConfigurator
from cybertools.wiki.base.wiki import WikiManager as BaseWikiManager
from cybertools.wiki.base.wiki import Wiki as BaseWiki
from cybertools.wiki.base.wiki import WikiPage as BaseWikiPage
from cybertools.wiki.interfaces import IWikiConfigInfo


class PersistentConfigInfo(PersistentMapping):

    implements(IWikiConfigInfo)

    def set(self, functionality, value):
        self[functionality] = value

    def __getattr__(self, attr):
        return self.get(attr, None)


class GenericConfigurator(BaseConfigurator):

    def initialize(self):
        ci = PersistentConfigInfo()
        self.context.setGenericAttribute('configInfo', ci)
        return ci

    def getConfigInfo(self):
        return self.context.getGenericAttribute('configInfo', None)


class WikiManager(BaseWikiManager):
    """
    """

    configurator = GenericConfigurator

    def setup(self):
        self.setGenericAttribute('wikis', IOTreeSet())
        plugins = self.setGenericAttribute('plugins', PersistentMapping())
        plugins[(IIntIds, '')] = IntIds()
        plugins[(ILinkManager, 'internal')] = LinkManager(self)
        self.setConfig('linkManager', 'internal')
        self.setConfig('preprocessor', ['mediawiki'])

    def addWiki(self, wiki):
        uid = self.getUid(wiki)
        self.wikiUids.insert(uid)
        wiki.setManager(self)
        return wiki

    def removeWiki(self, wiki):
        uid = self.getUid(wiki)
        if uid in self.wikiUids:
            self.wikiUids.remove(uid)

    def renameWiki(self, wiki, newName):
        wiki.rename(newName)

    def listWikis(self):
        for uid in self.wikiUids:
            yield self.getObject(uid)

    @Lazy
    def wikiUids(self):
        return self.getGenericAttribute('wikis')

    def getPlugins(self):
        return self.getGenericAttribute('plugins')

    def getObject(self, uid):
        obj = self.resolveUid(uid)
        if obj is None:
            return super(WikiManager, self).getObject(uid)
        return obj


class Wiki(BaseWiki):

    @property
    def name(self):
        return self.getId()

    def getPages(self):
        # TODO: restrict to wiki page objects
        return dict((k, v) for k, v in self.getItems())

    def createPage(self, name, title, text=u''):
        self[name] = self.pageFactory(name)
        page = self[name]
        page.title = title
        page.text = text
        return page

    def getManager(self):
        # provide in subclass
        raise NotImplementedError


class WikiPage(BaseWikiPage):

    def getText(self):
        return self.getGenericAttribute('text')
    def setText(self, text):
        self.setGenericAttribute('text', text)
    text = property(getText, setText)

    def getWiki(self):
        return self.getParent()


class LinkManager(BaseLinkManager):

    def __init__(self, manager):
        super(LinkManager, self).__init__()
        self.manager = manager

    def getUniqueId(self, obj):
        if obj is None:
            return None
        if isinstance(obj, self.uid):
            return obj
        return self.manager.getUid(obj)

    def getObject(self, uid):
        return self.manager.getObject(uid)

