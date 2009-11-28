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
Wiki implementation = adapters for Zope2 content objects.

$Id$
"""

try:
    from Acquisition import aq_inner, aq_parent
except ImportError:
    pass
from BTrees.IOBTree import IOTreeSet
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.cachedescriptors.property import Lazy
from zope import component
from zope.component import adapts
from zope.interface import implements

from cybertools.util.generic.interfaces import IGenericObject, IGenericFolder
from cybertools.wiki.base.config import WikiConfigInfo, BaseConfigurator
from cybertools.wiki.base.wiki import WikiManager as BaseWikiManager
from cybertools.wiki.base.wiki import Wiki as BaseWiki
from cybertools.wiki.base.wiki import WikiPage as BaseWikiPage
from cybertools.wiki.interfaces import ILinkManager, IWikiConfigInfo
from cybertools.wiki.tracking.link import Link, TrackingStorage


class PersistentConfigInfo(PersistentMapping):

    implements(IWikiConfigInfo)

    def set(self, functionality, value):
        self[functionality] = value

    def __getattr__(self, attr):
        return self.get(attr, None)


class GenericConfigurator(BaseConfigurator):

    def initialize(self):
        ci = PersistentConfigInfo()
        self.context.context.setGenericAttribute('configInfo', ci)
        return ci

    def getConfigInfo(self):
        return self.context.context.getGenericAttribute('configInfo', None)


class WikiManager(BaseWikiManager):

    adapts(IGenericObject)

    configurator = GenericConfigurator

    def __init__(self, context):
        self.context = context

    def setup(self):
        self.context.setGenericAttribute('wikis', IOTreeSet())
        plugins = self.context.setGenericAttribute('plugins', PersistentMapping())
        plugins[(IIntIds, None)] = IntIds()
        linkStorage = TrackingStorage(trackFactory=Link)
        plugins[(ILinkManager, 'tracking')] = linkStorage
        self.setConfig('linkManager', 'tracking')

    def addWiki(self, wiki):
        uid = self.getUid(wiki)
        self.wikiUids.insert(uid)
        wiki.setManager(self)
        return wiki

    def removeWiki(self, wiki):
        uid = self.getUid(wiki)
        if uid in self.wikiUids:
            self.wikiUids.remove(uid)

    def listWikis(self):
        for uid in self.wikiUids:
            yield self.getObject(uid)

    @Lazy
    def wikiUids(self):
        return self.context.getGenericAttribute('wikis')

    def getPlugins(self):
        return self.context.getGenericAttribute('plugins')

    def getUid(self, obj):
        return super(WikiManager, self).getUid(obj.context)

    def getObject(self, uid):
        obj = self.resolveUid(uid)
        if obj is None:
            co = super(WikiManager, self).getObject(uid)
            return co.typeInterface(co)
        return obj


class Wiki(BaseWiki):

    adapts(IGenericFolder)

    def __init__(self, context):
        self.context = context

    @property
    def name(self):
        return self.context.getId()

    @property
    def pages(self):
        # TODO: restrict to wiki page objects; use generic access methods
        return dict((k, WikiPage(v)) for k, v in self.context.objectItems())

    def createPage(self, name, title, text=u''):
        obj = self.context.pageFactory(name)
        page = WikiPage(obj)
        page.title = title
        page.text = text
        self.context._setObject(name, obj)
        return getattr(self.context, name)

    def getManager(self):
        # TODO: fetch tool/utility in a generic way
        co = self.context.portal_wikimanager
        return co.typeInterface(co)

    def absolute_url(self):
        return self.context.absolute_url()


class WikiPage(BaseWikiPage):

    adapts(IGenericFolder)

    def __init__(self, context):
        self.context = context

    def getTitle(self):
        return self.context.title
    def setTitle(self, title):
        self.context.title = title
    title = property(getTitle, setTitle)

    def getText(self):
        return self.context.text
    def setText(self, text):
        if self.context.getProperty('text') is None:
            self.context.manage_addProperty('text', text, 'text')
        else:
            self.context.manage_changeProperties(text=text)
    text = property(getText, setText)

    def getWiki(self):
        # TODO: fetch wiki in a generic way
        return Wiki(aq_parent(aq_inner(self.context)))
        #return Wiki(getParent(self.context))

    def absolute_url(self):
        return self.context.absolute_url()

