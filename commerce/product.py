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
Product classes.

$Id$
"""

from zope.interface import implements, Interface

from cybertools.commerce.common import RelationSet
from cybertools.commerce.interfaces import IProduct


class Product(object):

    implements(IProduct)

    collection = RelationSet

    def __init__(self, productId, title=None):
        self.name = self.productId = productId
        self.title = title or u'unknown'
        self.shops = self.collection(self, 'products')

