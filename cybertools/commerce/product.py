# cybertools.commerce.product

""" Product classes.
"""

from zope.interface import implementer, Interface

from cybertools.commerce.common import Relation, RelationSet, BaseObject
from cybertools.commerce.interfaces import IProduct, ICategory
from cybertools.commerce.interfaces import IManufacturer, ISupplier


@implementer(IProduct)
class Product(BaseObject):

    manufacturer = Relation('_manufacturer', 'products')

    def __init__(self, productId, title=None):
        self.name = self.productId = productId
        self.title = title or u'unknown'
        self.description = u''
        self.shops = self.collection(self, 'products')
        self.categories = self.collection(self, 'products')
        self.suppliers = self.collection(self, 'products')


@implementer(ICategory)
class Category(BaseObject):

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or u'unknown'
        self.description = u''
        self.shops = self.collection(self, 'categories')
        self.products = self.collection(self, 'categories')
        self.subcategories = self.collection(self, 'parentCategories')
        self.parentCategories = self.collection(self, 'subCategories')


@implementer(IManufacturer)
class Manufacturer(BaseObject):

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or u'unknown'
        self.products = self.collection(self, 'manufacturer')


@implementer(ISupplier)
class Supplier(BaseObject):

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or u'unknown'

