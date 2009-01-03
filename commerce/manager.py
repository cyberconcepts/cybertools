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
The commerce manager (container, registry, ...).

$Id$
"""

from zope.interface import implements

from cybertools.commerce.common import ContainerAttribute
from cybertools.commerce.customer import Customer
from cybertools.commerce.interfaces import IManager, IOrderItems
from cybertools.commerce.product import Product, Category, Manufacturer, Supplier
from cybertools.commerce.order import Order, OrderItem
from cybertools.commerce.shop import Shop
from cybertools.tracking.btree import TrackingStorage


class Manager(object):

    implements(IManager)

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


