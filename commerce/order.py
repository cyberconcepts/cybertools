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

from zope.app.intid.interfaces import IIntIds
from zope.cachedescriptors.property import Lazy
from zope import component
from zope.component import adapts
from zope.interface import implements, Interface

from cybertools.commerce.common import getUidForObject, getObjectForUid
from cybertools.commerce.common import Relation, BaseObject
from cybertools.commerce.interfaces import IOrder, IOrderItem, IOrderItems
from cybertools.tracking.btree import Track
from cybertools.tracking.interfaces import ITrackingStorage


class Order(BaseObject):

    implements(IOrder)

    customer = Relation('_customer', 'orders')

    def __init__(self, orderId, shop=None, customer=None):
        self.name = self.orderId = orderId
        self.shop = shop
        self.customer = customer


class OrderItem(Track):

    implements(IOrderItem)

    metadata_attributes = Track.metadata_attributes + ('order',)
    index_attributes = metadata_attributes
    typeName = 'OrderItem'

    def __getattr__(self, attr):
        if attr not in IOrderItem:
            raise AttributeError(attr)
        return self.data.get(attr)

    def getParent(self):
        return IOrderItems(self.__parent__)

    def getObject(self, ref):
        if isinstance(ref, int):
            return getObjectForUid(ref)
        if isinstance(ref, basestring):
            if ref.isdigit:
                return getObjectForUid(int(ref))
            if ':' in ref:
                tp, id = ref.split(':', 1)
                return (tp, id)
        return ref

    def remove(self):
        self.getParent().context.removeTrack(self)

    def modify(self, quantity, **kw):
        self.data['quantity'] = quantity
        return self

    def setOrder(self, order):
        parent = self.getParent()
        self.order = parent.getUid(order)
        parent.context.indexTrack(0, self, 'order')


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
            criteria['taskId'] = self.getUid(criteria.pop('product'))
        if 'party' in criteria:
            criteria['userName'] = self.getUid(criteria.pop('party'))
        if 'order' in criteria:
            criteria['order'] = self.getUid(criteria.pop('order'))
        if 'run' in criteria:
            criteria['runId'] = criteria.pop('run')
        return self.context.query(**criteria)

    def add(self, product, party, shop, order='???', run=0, **kw):
        kw['shop'] = self.getUid(shop)
        existing = self.getCart(party, order, shop, run, product=product)
        if existing:
            track = existing[-1]
            track.modify(track.quantity + kw.get('quantity', 1))
        else:
            trackId = self.context.saveUserTrack(self.getUid(product), run,
                                self.getUid(party), kw)
            track = self[trackId]
            track.order = self.getUid(order)
            self.context.indexTrack(0, track, 'order')
        return track

    def getCart(self, party=None, order='???', shop=None, run=None, **kw):
        if run:
            kw['run'] = run
        result = self.query(party=party, order=order, **kw)
        if shop is None:
            return list(result)
        shop = self.getUid(shop)
        return [item for item in result if item.shop == shop]

    # utility methods

    @Lazy
    def intIds(self):
        return component.getUtility(IIntIds)

    def getUid(self, obj):
        if isinstance(obj, BaseObject):
            return getUidForObject(obj, self.intIds)
        return obj

