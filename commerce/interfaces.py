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
Interfaces for the commerce domain like products, customers, orders, ...

$Id$
"""

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory

from cybertools.util.jeep import Jeep, Term

_ = MessageFactory('cybertools.commerce')


# shops

class IShop(Interface):
    """ A shop with products and customers.
    """

    name = schema.TextLine(
            title=_(u'Shop name'),
            description=_(u'An internal name uniquely identifying the shop.'),
            default=u'',
            required=True)
    title = schema.TextLine(
            title=_(u'Title'),
            description=_(u'Short title of the shop.'),
            default=u'',
            required=True)
    description = schema.Text(
            title=_(u'Description'),
            description=_(u'A medium-length description.'),
            default=u'',
            missing_value=u'',
            required=False)

    products = Attribute(u'The products available in this shop.')
    categories = Attribute(u'The product categories provided by this shop.')
    customers = Attribute(u'The customers registered for this shop.')


# products

class IProduct(Interface):
    """ A certain class of similar objects that may be put in a shopping cart.
    """

    productId = schema.TextLine(
            title=_(u'Product Identifier'),
            description=_(u'A name or number uniquely identifiying the '
                    u'product within a shop.'),
            default=u'',
            required=True)
    title = schema.TextLine(
            title=_(u'Title'),
            description=_(u'Short title of the product.'),
            default=u'',
            required=True)
    description = schema.Text(
            title=_(u'Description'),
            description=_(u'A medium-length description of the product.'),
            default=u'',
            missing_value=u'',
            required=False)

    categories = Attribute(u'The product categories this product belongs to.')
    shops = Attribute(u'The shops providing this product.')


class ICategory(Interface):
    """ A product category.
    """

    title = schema.TextLine(
            title=_(u'Title'),
            description=_(u'Short title of the category.'),
            default=u'',
            required=True)
    description = schema.Text(
            title=_(u'Description'),
            description=_(u'A medium-length description of the category.'),
            default=u'',
            missing_value=u'',
            required=False)

    products = Attribute(u'The products belonging to this category.')
    subcategories = Attribute(u'The sub-categories belonging to this category.')
    shops = Attribute(u'The shops providing this category.')


# customers

class ICustomer(Interface):
    """ A role of - for example - a person or institution (the ``client``)
        representing a customer of one or more shops.
    """

    customerId = schema.TextLine(
            title=_(u'Customer Identifier'),
            description=_(u'A name or number uniquely identifiying the customer.'),
            default=u'',
            required=True)

    client = Attribute(u'The (real) client object of the customer role.')
    shops = Attribute(u'The shops the client object is a customer of.')


# orders

class IOrder(Interface):
    """
    """

    orderId = Attribute(u'Order Identifier')
    shop = Attribute(u'The shop this order is for.')
    customer = Attribute(u'The customer issuing this order.')


class IOrderItem(Interface):
    """
    """

    order = Attribute(u'Order this order item belongs to.')
    product = Attribute(u'The product represented by this order item.')
    amount = Attribute(u'The number of product items ordered.')
    unitPrice = Attribute(u'The basic unit price for one of the product '
                    u'items ordered.')
