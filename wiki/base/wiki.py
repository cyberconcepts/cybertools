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
A Wiki manager managing wikis and wiki-related objects, esp plugins.

$Id$
"""

from zope import component
from zope.interface import implements
from zope.intid.interfaces import IIntIds
from zope.traversing.browser import absoluteURL

from cybertools.wiki.common import protocols, ExternalPage
from cybertools.wiki.interfaces import IWikiConfiguration
from cybertools.wiki.interfaces import IWikiManager, IWiki, IWikiPage
from cybertools.wiki.interfaces import IPreprocessor
from cybertools.wiki.interfaces import IParser, IWriter
from cybertools.wiki.base.config import BaseConfiguration


class WikiManager(BaseConfiguration):

    implements(IWikiManager)

    def __init__(self):
        self.setup()

    def setup(self):
        self.wikis = {}
        self.plugins = {}

    def addWiki(self, wiki):
        name = wiki.name
        if name in self.wikis:
            raise ValueError("Wiki '%s' already registered." % name)
        self.wikis[name] = wiki
        wiki.setManager(self)
        return wiki

    def removeWiki(self, wiki):
        name = wiki.name
        if name in self.wikis:
            del self.wikis[name]

    def renameWiki(self, wiki, newName):
        del self.wikis[wiki.name]
        self.wikis[newName] = wiki
        wiki.rename(newName)

    def listWikis(self):
        return self.wikis.values()

    def getPlugin(self, type, name=''):
        plugins = self.getPlugins()
        if (type, name) in plugins:
            plugin = plugins[(type, name)]
            if type is None:
                return plugin
            return type(plugin)
        return component.getUtility(type, name=name)

    def getPlugins(self):
        return self.plugins

    def getUid(self, obj):
        if isinstance(obj, ExternalPage):
            return obj.uid
        return self.getPlugin(IIntIds).register(obj)

    def getObject(self, uid):
        obj = self.resolveUid(uid)
        if obj is None:
            return self.getPlugin(IIntIds).getObject(int(uid))
        return obj

    def resolveUid(self, uid):
        if isinstance(uid, basestring):
            if ':' in uid:
                protocol, address = uid.split(':', 1)
                if protocol.lower() in protocols:
                    return ExternalPage(uid)
            if uid.startswith('/') or '..' in uid:
                return ExternalPage(uid)
        return None

    # configuration

    def getConfigParent(self):
        return component.getUtility(IWikiConfiguration)


class Wiki(BaseConfiguration):

    implements(IWiki)

    manager = None

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or name
        self.pages = {}

    def setup(self):
        self.getManager().addWiki(self)
        self.createPage('StartPage', u'Start Page',
                        u'The text of the **Start Page**')

    def getManager(self):
        return self.manager

    def setManager(self, manager):
        self.manager = manager

    def createPage(self, name, title=None):
        if name in self.pages:
            raise ValueError("Name '%s' already present." % name)
        page = self.pages[name] = WikiPage(name)
        page.wiki = self
        page.title = title or name
        return page

    def addPage(self, page):
        self.pages[page.name] = page
        page.wiki = self
        return page

    def removePage(self, name):
        if name in self.pages:
            del self.pages[name]

    def getPage(self, name):
        if ':' in name:
            protocol, address = name.split(':', 1)
            if protocol in protocols:
                return ExternalPage(name)
        return self.getPages().get(name)

    def listPages(self):
        return self.getPages().values()

    def getPages(self):
        return self.pages

    # configuration

    def getConfigParent(self):
        return self.getManager()


class WikiPage(BaseConfiguration):

    implements(IWikiPage)

    wiki = None
    text = u''

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or name
        self.setup()

    def setup(self):
        pass

    def getWiki(self):
        return self.wiki

    def render(self, request=None):
        # TODO: move render() method to a view class
        source = self.preprocess(self.text)
        tree = self.parse(source, request)
        result = self.write(tree)
        return self.postprocess(result)

    def parse(self, source, request=None):
        parserName = self.getConfig('parser')
        parser = component.getUtility(IParser, name=parserName)
        return parser.parse(source, self, request)

    def write(self, tree):
        writerName = self.getConfig('writer')
        writer = component.getUtility(IWriter, name=writerName)
        return writer.write(tree)

    def preprocess(self, text):
        preprocs = self.getConfig('preprocessor') or []
        for name in preprocs:
            pp = component.getUtility(IPreprocessor, name=name)
            text = pp(text)
        return text

    def postprocess(self, result):
        return result

    # IWebResource

    @property
    def uid(self):
        return self.getUid()

    def getUid(self):
        return self.getWiki().getManager().getUid(self)

    def getURI(self, request):
        return absoluteURL(self, request)

    # configuration

    def getConfigParent(self):
        return self.getWiki()

