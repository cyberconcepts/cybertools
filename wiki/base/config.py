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
Basic Configuration implementations.

$Id$
"""

from zope.interface import implements

from cybertools.wiki.interfaces import IWikiConfiguration


class BaseConfiguration(object):
    """ The base class for all wiki configuration implementations.
    """

    implements(IWikiConfiguration)

    parent = None

    writer = parser = None

    def getConfig(self, functionality):
        c = self.get(functionality)
        if c is None:
            parent = self.getConfigParent()
            if parent is not None:
                return parent.getConfig(functionality)
        return c

    def get(self, key, default=None):
        return getattr(self, key, None)

    def getConfigParent(self):
        return self.parent


class WikiConfiguration(BaseConfiguration):
    """ A global utility providing the default settings.
    """

    writer = 'docutils.html'
    parser = 'docutils.rstx'
    processor = 'standard'
    linkManager = 'basic'

    nodeProcessors = dict(reference=['default'])
