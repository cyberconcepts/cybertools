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

    name = schema.ASCII(
            title=_(u'Shop name'),
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

    name = schema.ASCII(
            title=_(u'Supplier name'),
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
            description=_(u'A name or number uniquely identifiying the '
                    u'product within a shop.'),
            default='',
            required=True)
    title = schema.TextLine(
            title=_(u'Artikelname'),
            description=_(u'Artikelname'),
            default=u'',
            required=True)
    manufnumber = schema.TextLine(
            title=_(u'Manufacturer Number'),
            description=_(u'Manufacturer Number'),
            default=u'',
            required=False)
    headline = schema.TextLine(
            title=_(u'Headline'),
            description=_(u'special headline'),
            default=u'',
            required=False)
    description = schema.Text(
            title=_(u'Description'),
            description=_(u'Description'),
            default=u'',
            missing_value=u'',
            required=False)
    fullDescription = schema.Text(
            title=_(u'Full Description'),
            description=_(u'Full Description'),
            default=u'',
            required=False)
    advantages = schema.Text(
            title=_(u'Advantages'),
            description=_(u'Advantages'),
            default=u'',
            missing_value=u'',
            required=False)
    includes = schema.Text(
            title=_(u'Includes'),
            description=_(u'Includes'),
            default=u'',
            missing_value=u'',
            required=False)
    remarks = schema.Text(
            title=_(u'Remarks'),
            description=_(u'Remarks'),
            default=u'',
            missing_value=u'',
            required=False)
    intremarks = schema.Text(
            title=_(u'internal Remarks'),
            description=_(u'internal Remarks'),
            default=u'',
            missing_value=u'',
            required=False)
    manufwarranty = schema.TextLine(
            title=_(u'Manufacturer Warranty'),
            description=_(u'Manufacturer Warranty'),
            default=u'',
            required=False)
    warranty = schema.Choice(
            title=_(u'Warranty'),
            description=_(u'Warranty'),
            source=util.KeywordVocabulary((
                    ('w1', _(u'14 Tage')),
                    ('w2', _(u'3 Monate')),
                    ('w3', _(u'6 Monate')),
                    ('w4', _(u'1 Jahr')),
                    ('w5', _(u'2 Jahre')),
                    ('w6', _(u'3 Jahre')),
                    ('w7', _(u'4 Jahre')),
                    ('w8', _(u'5 Jahre')),
                    ('w9', _(u'6 Jahre')),
                    ('w10', _(u'Keine Garantie')),
                    ('w11', _(u'Wie Einzelartikel')),
                )),
            default=u'w1',
            required=True)
    originalwarranty = schema.Choice(
            title=_(u'Original Warranty'),
            description=_(u'Original Warranty'),
            source=util.KeywordVocabulary((
                    ('ow1', _(u'14 Tage')),
                    ('ow2', _(u'3 Monate')),
                    ('ow3', _(u'6 Monate')),
                    ('ow4', _(u'1 Jahr')),
                    ('ow5', _(u'2 Jahre')),
                    ('ow6', _(u'3 Jahre')),
                    ('ow7', _(u'4 Jahre')),
                    ('ow8', _(u'5 Jahre')),
                    ('ow9', _(u'6 Jahre')),
                    ('ow10', _(u'Keine Garantie')),
                    ('ow11', _(u'Wie Einzelartikel')),
                )),
            default=u'ow1',
            required=True)
    state = schema.Choice(
            title=_(u'State'),
            description=_(u'State'),
            source=util.KeywordVocabulary((
                    ('1', _(u'Im Programm')),
                    ('2', _(u'Bald im Programm')),
                    ('3', _(u'Nicht im Programm')),
                )),
            default=u'1',
            required=True)
    oldstock = schema.Bool(
            title=_(u'Old Stock'),
            description=_(u'Old Stock'),
            required=False)
    retail = schema.Bool(
            title=_(u'Retail'),
            description=_(u'Reatil'),
            required=False)
    notinstock = schema.Bool(
            title=_(u'Not In Stock'),
            description=_(u'Not In Stock'),
            required=False)
    rohs = schema.Bool(
            title=_(u'RoHS'),
            description=_(u'RoHS'),
            required=False)
    takepicture = schema.Bool(
            title=_(u'Take Picture'),
            description=_(u'Take Picture'),
            required=False)
    stocklist = schema.TextLine(
            title=_(u'Stocklist'),
            description=_(u'Stocklist'),
            default=u'',
            required=False)
    special = schema.TextLine(
            title=_(u'Special'),
            description=_(u'Special'),
            default=u'',
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
    """ A role of - for example - a person or institution (the ``client``)
        representing a customer of one or more shops.
    """

    customerId = schema.ASCII(
            title=_(u'Customer Identifier'),
            description=_(u'A name or number uniquely identifiying the customer.'),
            default='',
            required=True)

    client = Attribute(u'The (real) client object of the customer role.')
    shops = Attribute(u'The shops the client object is a customer of.')


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
