#
#  Copyright (c) 2011 Helmut Merz helmutm@cy55.de
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

""" URL manipulation utilities

$Id$
"""

from urlparse import urlparse

from zope.app.container.traversal import ItemTraverser
from zope.interface import Interface, implements


TraversalRedirector(ItemTraverser):

    port = 9083
    names = ('ctt', 'sona',)
    loc_pattern = 'www.%s.de'
    skip = (0, 4)

    def publishTraverse(self, request, name):
        return super(TraversalRedirector, self).publishTraverse(request, name)
