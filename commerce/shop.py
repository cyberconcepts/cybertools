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
Base classes.

$Id$
"""

from zope.interface import implements

from cybertools.commerce.common import RelationSet, BaseObject
from cybertools.commerce.interfaces import IShop


class Shop(BaseObject):

    implements(IShop)

    collection = RelationSet

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or u'Shop'
        self.products = self.collection(self, 'shops')
        self.customers = self.collection(self, 'shops')
