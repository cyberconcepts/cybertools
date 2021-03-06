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
Customer classes.

$Id$
"""

from zope.interface import implements, Interface

from cybertools.commerce.common import RelationSet, BaseObject
from cybertools.commerce.interfaces import ICustomer, IAddress


class Customer(BaseObject):

    implements(ICustomer)

    def __init__(self, customerId, title=None, client=None):
        self.name = self.customerId = customerId
        self.title = title or u'unknown'
        self.client = client
        self.shops = self.collection(self, 'customers')
        self.orders = self.collection(self, 'customer')


class Address(BaseObject):

    implements(IAddress)

