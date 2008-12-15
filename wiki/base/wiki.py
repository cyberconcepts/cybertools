#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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

from docutils.core import publish_doctree, publish_from_doctree
from docutils.writers.html4css1 import HTMLTranslator, Writer
from zope.interface import implements

from cybertools.wiki.interfaces import IWikiManager, IWiki, IWikiPage


class WikiManager(object):

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


class Wiki(object):

    implements(IWiki)

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


class WikiPage(object):

    implements(IWikiPage)

    text = u''

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or name

    def render(self):
        return self.write(self.parse())

    def parse(self):
        # TODO: delegate to parser plugin
        return publish_doctree(self.text)

    def write(self, tree):
        # TODO: delegate to writer plugin, use translator plugins
        writer = Writer()
        writer.translator_class = HTMLBodyTranslator
        return publish_from_doctree(tree, writer=writer)


class HTMLBodyTranslator(HTMLTranslator):

    def astext(self):
        return u''.join(self.body_pre_docinfo + self.docinfo + self.body)