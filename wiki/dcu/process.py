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
Node processor implementations for docutils nodes.

$Id: process.py 3153 2009-01-17 16:51:09Z helmutm $
"""

from docutils.nodes import Text
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope.interface import implements

from cybertools.wiki.base.link import LinkProcessor
from cybertools.wiki.dcu.html import HTMLReferenceNode


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

    def setURI(self, uri):
        self.context.atts['href'] = uri

    def markPresentation(self, feature):
        self.context.atts['class'] += (' ' + feature)

    def addText(self, text):
        self.context.node.insert(0, Text(text))
