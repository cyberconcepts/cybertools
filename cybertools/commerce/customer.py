# cybertools.commerce.customer

""" Customer classes.
"""

from zope.interface import implementer, Interface

from cybertools.commerce.common import RelationSet, BaseObject
from cybertools.commerce.interfaces import ICustomer, IAddress


@implementer(ICustomer)
class Customer(BaseObject):

    def __init__(self, customerId, title=None, client=None):
        self.name = self.customerId = customerId
        self.title = title or u'unknown'
        self.client = client
        self.shops = self.collection(self, 'customers')
        self.orders = self.collection(self, 'customer')


@implementer(IAddress)
class Address(BaseObject):

    pass

