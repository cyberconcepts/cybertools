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
Product classes.

$Id$
"""

from zope.interface import implements, Interface

from cybertools.commerce.common import Relation, RelationSet, BaseObject
from cybertools.commerce.interfaces import IProduct, ICategory
from cybertools.commerce.interfaces import IManufacturer, ISupplier


class Product(BaseObject):

    implements(IProduct)

    manufacturer = Relation('_manufacturer', 'products')

    def __init__(self, productId, title=None):
        self.name = self.productId = productId
        self.title = title or u'unknown'
        self.description = u''
        self.shops = self.collection(self, 'products')
        self.categories = self.collection(self, 'products')
        self.suppliers = self.collection(self, 'products')


class Category(BaseObject):

    implements(ICategory)

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or u'unknown'
        self.description = u''
        self.shops = self.collection(self, 'categories')
        self.products = self.collection(self, 'categories')
        self.subcategories = self.collection(self, 'parentCategories')
        self.parentCategories = self.collection(self, 'subCategories')


class Manufacturer(BaseObject):

    implements(IManufacturer)

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or u'unknown'
        self.products = self.collection(self, 'manufacturer')


class Supplier(BaseObject):

    implements(ISupplier)

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or u'unknown'

