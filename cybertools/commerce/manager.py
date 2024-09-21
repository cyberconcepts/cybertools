# cybertools.commerce.manager

""" The commerce manager (container, registry, ...).
"""

from zope.interface import implementer

from cybertools.commerce.common import ContainerAttribute
from cybertools.commerce.customer import Customer
from cybertools.commerce.interfaces import IManager, IOrderItems
from cybertools.commerce.product import Product, Category, Manufacturer, Supplier
from cybertools.commerce.order import Order, OrderItem
from cybertools.commerce.shop import Shop
from cybertools.tracking.btree import TrackingStorage


@implementer(IManager)
class Manager(object):

    def __init__(self):
        self.shops = ContainerAttribute(Shop)
        self.products = ContainerAttribute(Product, 'productId')
        self.categories = ContainerAttribute(Category, 'name')
        self.manufacturers = ContainerAttribute(Manufacturer, 'name')
        self.suppliers = ContainerAttribute(Supplier, 'name')
        self.customers = ContainerAttribute(Customer, 'customerId')
        self.orders = ContainerAttribute(Order, 'orderId')
        self._orderItems = TrackingStorage(trackFactory=OrderItem)

    @property
    def orderItems(self):
        return IOrderItems(self._orderItems)


