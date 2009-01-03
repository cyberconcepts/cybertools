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
Order and order item classes.

$Id$
"""

from zope.component import adapts
from zope.interface import implements, Interface

from cybertools.commerce.common import Relation, BaseObject
from cybertools.commerce.interfaces import IOrder, IOrderItem, IOrderItems
from cybertools.tracking.btree import Track
from cybertools.tracking.interfaces import ITrackingStorage


class Order(object):

    implements(IOrder)

    customer = Relation('_customer', 'orders')

    def __init__(self, orderId, shop=None, customer=None):
        self.name = self.orderId = orderId
        self.shop = shop
        self.customer = customer


class OrderItem(Track):

    implements(IOrderItem)

    def __getattr__(self, attr):
        if attr not in IOrderItem:
            raise AttributeError(attr)
        return self.data.get(attr)


class OrderItems(object):
    """ A tracking storage adapter managing order items.
    """

    implements(IOrderItems)
    adapts(ITrackingStorage)

    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        return self.context[key]

    def __iter__(self):
        return iter(self.context.values())

    def query(self, **criteria):
        if 'product' in criteria:
            criteria['taskId'] = criteria.pop('product')
        if 'person' in criteria:
            criteria['userName'] = criteria.pop('person')
        if 'run' in criteria:
            criteria['runId'] = criteria.pop('run')
        return self.context.query(**criteria)

    def add(self, product, person, run=0, **kw):
        trackId = self.context.saveUserTrack(product, run, person, kw)
        track = self[trackId]
        return track
