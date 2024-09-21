# cybertools.commerce.shop

""" Base classes.
"""

from zope.interface import implementer

from cybertools.commerce.common import RelationSet, BaseObject
from cybertools.commerce.interfaces import IShop


@implementer(IShop)
class Shop(BaseObject):

    collection = RelationSet

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or u'Shop'
        self.products = self.collection(self, 'shops')
        self.customers = self.collection(self, 'shops')
        self.orderNumber = 0

    def getNewOrderId(self):
        last = self.orderNumber or 0
        num = last + 1
        self.orderNumber = num
        return '%05i' % num
