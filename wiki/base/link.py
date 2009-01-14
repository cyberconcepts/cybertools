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

from zope.interface import implements

from cybertools.wiki.interfaces import ILink, ILinkManager


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
        self.linksBySource[source] = self.links[id] = link

    def removeLink(self, link):
        if link.identifier in self.links:
            link.manager = None
            del self.links[link.identifier]

    def generateLinkIdentifier(self, link):
        identifier = 'l%07i' % (max(self.links.keys() or [0]) + 1)
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
        return getattr(self, attr, None)

