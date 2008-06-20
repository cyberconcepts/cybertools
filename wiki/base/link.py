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
Basic (sample) implementations for links and link management

$Id$
"""

import re
from zope.interface import implements

from cybertools.wiki.interfaces import ILink, ILinkFormat, ILinkManager


class Link(object):

    implements(ILink)

    identifier = None
    manager = None
    formatName = None

    def __init__(self, source, target):
        self.source = source
        self.target = target


class BaseLinkFormat(object):

    implements(ILinkFormat)

    manager = None

    name = 'base'
    internalFormat = '##%s##'
    internalRegexp = re.compile(r'##(.+)##(.+)##')

    def __init__(self, context):
        self.context = context

    def unmarshall(self, text):
        return self.externalRegexp.sub(self.processLink, text)

    def marshall(self, text):
        return text

    def display(self, text):
        return text

    def processLink(self, match):
        ref, label = match.group(1).split(' ', 1)
        link = Link(self.context, ref)
        link.original = match.group(0)
        link.label = label
        self.manager.register(link)
        return self.externalFormat % (self.internalFormat % link.identifier)


class DoubleBracketLinkFormat(BaseLinkFormat):

    name = 'doublebracket'
    externalFormat = '[[%s]]'
    externalRegexp = re.compile(r'\[\[(.+)\]\]')


class LinkManager(object):

    implements(ILinkManager)

    def __init__(self):
        self.links = {}

    def register(self, link):
        if link.identifier is None:
            self.generateIdentifier(link)
        if link.identifier not in self.links:
            self.links[link.identifier] = link
            link.manager = self

    def unregister(self, link):
        if link.identifier in self.links:
            del self.links[link.identifier]
            link.manager = None

    def generateIdentifier(self, link):
        identifier = '%07i' % (max(self.links.keys() or [0]) + 1)
        link.identifier = identifier
        return identifier

