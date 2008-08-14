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
from loops import util
from cybertools.util.jeep import Jeep, Term
from loops import util

_ = MessageFactory('cybertools.commerce')


# shops

class IShop(Interface):
    """ A shop with products and customers.
    """

    name = schema.ASCIILine(
            title=_(u'Shop Identifier'),
            description=_(u'An internal name uniquely identifying the shop.'),
            default='',
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
            required=False)

    products = Attribute(u'The products available in this shop.')
    categories = Attribute(u'The product categories provided by this shop.')
    suppliers = Attribute(u'The suppliers providing products for '
                    u'this shop.')
    customers = Attribute(u'The customers registered for this shop.')


# suppliers

class ISupplier(Interface):
    """ Manufactures or supplies products.
    """

    name = schema.ASCIILine(
            title=_(u'Supplier Identifier'),
            description=_(u'An internal name uniquely identifying the supplier.'),
            default='',
            required=True)
    title = schema.TextLine(
            title=_(u'Title'),
            description=_(u'Short title of the supplier.'),
            default=u'',
            required=True)
    description = schema.Text(
            title=_(u'Description'),
            description=_(u'A medium-length description.'),
            default=u'',
            missing_value=u'',
            required=False)

    products = Attribute(u'The products provided by this supplier.')
    categories = Attribute(u'The primary product categories this supplier '
                    u'provides products of.')


# products

class IProduct(Interface):
    """ A certain class of similar objects that may be put in a shopping cart.
    """

    productId = schema.ASCIILine(
            title=_(u'Product Identifier'),
            description=_(u'A name or number uniquely identifiying the product.'),
            default='',
            required=True)
    title = schema.TextLine(
            title=_(u'Product Name'),
            description=_(u'Product name.'),
            default=u'',
            required=True)
    description = schema.Text(
            title=_(u'Description'),
            description=_(u'A medium-length description.'),
            default=u'',
            missing_value=u'',
            required=False)
    fullDescription = schema.Text(
            title=_(u'Full Description'),
            description=_(u'A Detailled description of the product.'),
            default=u'',
            required=False)
    remarks = schema.Text(
            title=_(u'Remarks'),
            description=_(u'Some additional remarks.'),
            default=u'',
            missing_value=u'',
            required=False)

    categories = Attribute(u'The product categories this product belongs to.')
    suppliers = Attribute(u'The suppliers (typically only one) providing '
                    u'this product.')
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
    suppliers = Attribute(u'The suppliers providing products of this category.')


# customers

class ICustomer(Interface):
    """ Typically a role of - for example - a person or institution (the ``client``)
        representing a customer of one or more shops.

        The client may be None in which case the customer is an object on
        its own.
    """

    customerId = schema.ASCIILine(
            title=_(u'Customer Identifier'),
            description=_(u'A name or number uniquely identifiying the customer.'),
            default='',
            required=True)
    title = schema.TextLine(
            title=_(u'Customer Name'),
            description=_(u'Customer name.'),
            default=u'',
            required=True)
    description = schema.Text(
            title=_(u'Description'),
            description=_(u'A medium-length description of the category.'),
            default=u'',
            missing_value=u'',
            required=False)

    shops = Attribute(u'The shops the client object is a customer of.')

    client = Attribute(u'An optional (real) client object of the customer role.')


# orders

class IOrder(Interface):
    """
    """

    orderId = Attribute(u'Order Identifier')
    shop = Attribute(u'The shop this order belongs to.')
    customer = Attribute(u'The customer issuing this order.')


class IOrderItem(Interface):
    """
    """

    quantity = schema.Int(
            title=_(u'Quantity'),
            description=_(u'The number of product items ordered.'),
            default=1,
            required=True)

    order = Attribute(u'Order this order item belongs to.')
    product = Attribute(u'The product represented by this order item.')
    unitPrice = Attribute(u'The basic unit price for one of the product '
                    u'items ordered.')
