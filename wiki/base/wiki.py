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
A Wiki manager managing wikis and wiki-related objects, esp plugins.

$Id$
"""

from zope import component
from zope.interface import implements
from zope.app.intid.interfaces import IIntIds

from cybertools.wiki.interfaces import IWikiConfiguration
from cybertools.wiki.interfaces import IWikiManager, IWiki, IWikiPage
from cybertools.wiki.interfaces import IParser, IWriter, ITreeProcessor
from cybertools.wiki.base.config import BaseConfiguration


class WikiManager(BaseConfiguration):

    implements(IWikiManager)

    def __init__(self):
        self.wikis = {}

    def addWiki(self, wiki):
        name = wiki.name
        if name in self.wikis:
            raise ValueError("Wiki '%s' already registered." % name)
        self.wikis[name] = wiki
        wiki.manager = self
        return wiki

    def removeWiki(self, wiki):
        name = wiki.name
        if name in self.wikis:
            del self.wikis[name]

    def listWikis(self):
        return self.wikis.values()

    def getPlugin(self, type, name):
        return component.getUtility(type, name=name)

    def getUid(self, obj):
        return component.getUtility(IIntIds).getId(obj)

    def getObject(self, uid):
        return component.getUtility(IIntIds).getObject(uid)

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

    def getManager(self):
        return self.manager

    def createPage(self, name, title=None):
        if name in self.pages:
            raise ValueError("Name '%s' already present." % name)
        page = self.pages[name] = WikiPage(name, title)
        page.wiki = self
        return page

    def removePage(self, name):
        if name in self.pages:
            del self.pages[name]

    def getPage(self, name):
        return self.pages.get(name)

    def listPages(self):
        return self.pages.values()

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

    def getWiki(self):
        return self.wiki

    def render(self, request=None):
        source = self.preprocess(self.text)
        tree = self.parse(source)
        self.process(tree, request)
        result = self.write(tree)
        return self.postprocess(result)

    def parse(self, source):
        parserName = self.getConfig('parser')
        parser = component.getUtility(IParser, name=parserName)
        return parser.parse(source)

    def write(self, tree):
        writerName = self.getConfig('writer')
        writer = component.getUtility(IWriter, name=writerName)
        return writer.write(tree)

    def preprocess(self, source):
        return source

    def process(self, tree, request=None):
        processor = component.getAdapter(self, ITreeProcessor,
                                         name=self.getConfig('processor'))
        processor.tree = tree
        processor.request = request
        processor.process()

    def postprocess(self, result):
        return result

    # configuration

    def getConfigParent(self):
        return self.getWiki()

