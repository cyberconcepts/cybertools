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
A Wiki manager, i.e. a repository for pages and other information like
links, images, etc.

$Id$
"""

from zope.interface import implements

from cybertools.wiki.interfaces import IWikiManager


class SampleManager(object):
    """ A very basic Wiki manager implementation.
    """

    def __init__(self):
        self.links = {}

    def registerLink(self, link):
        if link.identifier is None:
            self.generateLinkIdentifier(link)
        if link.identifier not in self.links:
            self.links[link.identifier] = link
            link.manager = self

    def unregisterLink(self, link):
        if link.identifier in self.links:
            del self.links[link.identifier]
            link.manager = None

    def generateLinkIdentifier(self, link):
        identifier = 'l%07i' % (max(self.links.keys() or [0]) + 1)
        link.identifier = identifier
        return identifier