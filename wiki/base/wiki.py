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

    # configuration

    def getParent(self):
        return component.getUtility(IWikiConfiguration)


class Wiki(BaseConfiguration):

    implements(IWiki)

    manager = None

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or name
        self.pages = {}

    def createPage(self, name, title=None):
        if name in self.pages:
            raise ValueError("Name '%s' already present." % name)
        page = self.pages[name] = WikiPage(name, title)
        page.wiki = self
        return page

    # configuration

    def getParent(self):
        return self.manager


class WikiPage(BaseConfiguration):

    implements(IWikiPage)

    wiki = None
    text = u''

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or name

    def render(self):
        source = self.preprocess(self.text)
        tree = self.parse(source)
        self.process(tree)
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

    def process(self, tree):
        processor = component.getAdapter(self, ITreeProcessor,
                                         name=self.getConfig('processor'))
        processor.tree = tree
        processor.process()

    def postprocess(self, result):
        return result

    # configuration

    def getParent(self):
        return self.wiki

