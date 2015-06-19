#-*- coding: UTF-8 -*-
#
#  Copyright (c) 2015 Helmut Merz helmutm@cy55.de
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
"""

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory

from cybertools.util.jeep import Jeep, Term
from cybertools.organize.interfaces import IAddress as IBaseAddress
from cybertools.organize.interfaces import IPerson as IBasePerson
from cybertools.tracking.interfaces import ITrack
from loops import util

_ = MessageFactory('cybertools.commerce')


# manager

class IManager(Interface):
    """ A top-level container, registry, manager that provides access to
        all components of a commerce site.
    """

    shops = Attribute(u'All shops in this commerce manager.')
    products = Attribute(u'All products in this commerce manager.')
    categories = Attribute(u'All product categories in this commerce manager.')
    manufacturers = Attribute(u'All manufacturers in this commerce manager.')
    suppliers = Attribute(u'All suppliers in this commerce manager.')
    customers = Attribute(u'All customers in this commerce manager.')
    orders = Attribute(u'All orders in this commerce manager.')
    orderItems = Attribute(u'All order items; may also be cart items without '
                u'relation to an existing order.')


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
    orderNumber = schema.Int(
            title=_(u'Order Number'),
            description=_(u'The number used for the order identifier of '
                          u'last order created. This will in turn be used '
                          u'for creating the next order identifier.'),
            default=0,
            required=False)
    defaultPriceScale = schema.ASCIILine(
            title=_(u'Default Price Scale'),
            description=_(u'A string specifying the price '
                    u'scale that should be used if the user is not '
                    u'related to a customer or the customer does not have '
                    u'a price group.'),
            default='',
            required=False)
    priceMarkup= schema.Float(
            title=_(u'Price Markup (%)'),
            description=_(u'Markup in percent to apply to the standard price of the product '
                    u'if the product has not got a price for the price scale given.'),
            default=0.0,
            required=False)
    isConsumerShop = schema.Bool(
            title=_(u'Is Consumer Shop'),
            description=_(u'Check if shop is primarily for consumers.'),
            default=False,
            required=False)
    email = schema.TextLine(
            title=_(u'E-Mail Address'),
            description=_(u'Email address of the shop.'),
            default=u'',
            required=False)

    products = Attribute(u'The products available in this shop.')
    categories = Attribute(u'The product categories provided by this shop.')
    manufacturers = Attribute(u'The manufacturers whose products are available '
                    u'in this shop.')
    suppliers = Attribute(u'The suppliers providing products for '
                    u'this shop.')
    customers = Attribute(u'The customers registered for this shop.')

    def getNewOrderId():
        """ Create a new order identifier.
        """


# manufacturers and suppliers

class IManufacturer(Interface):
    """ Produces products.
    """

    name = schema.ASCIILine(
            title=_(u'Supplier Identifier'),
            description=_(u'An internal name uniquely identifying the manufacturer.'),
            default='',
            required=True)
    title = schema.TextLine(
            title=_(u'Title'),
            description=_(u'Short title of the manufacturer.'),
            default=u'',
            required=True)
    description = schema.Text(
            title=_(u'Description'),
            description=_(u'A medium-length description.'),
            default=u'',
            missing_value=u'',
            required=False)

    products = Attribute(u'The products provided by this manufacturer.')
    categories = Attribute(u'The primary product categories this manufacturer '
                    u'provides products of.')


class ISupplier(Interface):
    """ Supplies products.
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
    manufacturer = Attribute(u'The manufacturer providing this product.')
    suppliers = Attribute(u'The suppliers (typically only one) providing '
                    u'this product.')
    shops = Attribute(u'The shops providing this product.')


class ICategory(Interface):
    """ A product category.
    """

    name = schema.ASCIILine(
            title=_(u'Category Identifier'),
            description=_(u'An internal name uniquely identifying the category.'),
            default='',
            required=True)
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
    order = schema.Int(
            title=_(u'Sortingorder'),
            description=_(u'Sortingorder'),
            default=0,
            required=False)
    visible = schema.Bool(
            title=_(u'Visible'),
            description=_(u'Visible in Menu'),
            default=True,
            required=False)

    products = Attribute(u'The products belonging to this category.')
    subcategories = Attribute(u'The sub-categories belonging to this category.')
    parentCategories = Attribute(u'The parent categories belonging to this category.')
    shops = Attribute(u'The shops providing this category.')
    accessories = Attribute(u'Accessories for this category.')


# customers

class ICustomer(Interface):
    """ Typically a role instance of - for example - a person or institution
        (the ``client``) representing a customer of one or more shops.

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
            description=_(u'A medium-length description of the customer.'),
            default=u'',
            missing_value=u'',
            required=False)

    shops = Attribute(u'The shops the client object is a customer of.')
    paymentTypes = Attribute(u'A collection of payment types supported.')
    orders = Attribute(u'A collection of the customer\'s orders.')

    client = Attribute(u'An optional (real) client object of the customer role.')


class IPerson(IBasePerson):

    customer = Attribute(u'The customer the person belongs to.')


addressTypesVoc = util.KeywordVocabulary((
        ('standard', _(u'Standard Address')),
        ('invoice', _(u'Invoice Address')),
        ('shipping', _(u'Shipping Address')),
        ('defaultShipping', _(u'Default Shipping Address')),
))


class IAddress(IBaseAddress):

    addressType = schema.Choice(
            title=_(u'Address Type'),
            description=_(u'Address type.'),
            source=addressTypesVoc,
            default='standard',
            required=False)

    clients = Attribute(u'A collection of objects that this address belongs to.')

# orders

valueTypesVoc = util.KeywordVocabulary((
        ('product', _(u'Product Prices')),
        ('shipping', _(u'Shipping Cost')),
))

vatRatesVoc = util.KeywordVocabulary((
        ('product', 0),
        ('reduced', 7),
        ('standard', 19),
))


currencyVoc = util.KeywordVocabulary((
        ('EUR', u'€'),
        ('USD', u'$'),
))


class IValue(Interface):
    """ An order or item value with additional information about the type of
        the value and e.g. the VAT rate.
    """

    type = Attribute(u'The type of the value; see valueTypesVoc.')
    value = Attribute(u'The value in the standard currency (EUR), '
                u'stored as a Decimal value.')
    currency = Attribute(u'The currency of the value.')
    currencyRate = Attribute(u'The rate for converting the value to the '
                u'standard currency, default is 1.')
    vat = Attribute(u'The id of the VAT rate; see vatRatesVoc.')


class IOrder(Interface):
    """
    """

    orderId = schema.TextLine(title=u'Order Identifier')
    orderDate = schema.Date(
            title=u'Order Date',
            description=u'The day the order was issued.')
    paymentType = schema.TextLine(
            title=u'Payment Type',
            description=u'The payment type to be used for the order.')
    paymentId = schema.TextLine(
            title=u'Payment ID',
            description=u'A string identifying the payment transaction.')
    paymentTransactionId = schema.TextLine(
            title=u'Payment Transaction ID',
            description=u'The transaction ID provided by the payment service.')
    shipmentMode = schema.TextLine(
            title=u'Shipment Mode',
            description=u'The mode of shipment to be used for the order.')
    state = schema.TextLine(
            title=u'State',
            description=u'A string specifying the state of the order.')
    comments = schema.Text(
            title=u'Comments',
            description=u'Some arbitrary text associated with the order.')

    shop = Attribute(u'The shop this order belongs to.')
    customer = Attribute(u'The customer issuing this order.')
    invoiceAddress = Attribute(u'The address the invoice should be sent to.')
    shippingAddress = Attribute(u'The address the products should be sent to.')

    shippingCost = Attribute(u'The cost to be applied for shipping.')
    additionalCost = Attribute(u'An additional value to be added to the '
                        u'net value of the order.')
    additionalCost2 = Attribute(u'A second additional value to be added to '
                        u'the net value of the order.')
    tax = Attribute(u'The tax value to be added to the net value of the order.')
    total = Attribute(u'The total gross value (Decimal) of the order.')

    # not implemented yet
    netValues = Attribute(u'A collection of net total values (IValue objects)'
                u'of the order.')
    orderType = Attribute(u'Some string used for identifying the type of the order.')


class IOrderItem(ITrack):
    """ An individual order or cart item.
    """

    quantity = schema.Int(
            title=_(u'Quantity'),
            description=_(u'The number of product items ordered.'),
            default=1,
            required=True)

    product = Attribute(u'The product represented by this order item.')
    productTitle = Attribute(u'Optional short description, especially '
                u'useful for pseudo products.')
    party = Attribute(u'The party (person, customer, session, ...) '
                u'that is ordering the product.')
    shop = Attribute(u'The shop from which the product is ordered.')
    order = Attribute(u'The order this order item belongs to.')
    unitPrice = Attribute(u'The basic unit price for one of the product '
                    u'ites ordered.')
    fullPrice = Attribute(u'The full price for the quantity ordered.')
    quantityShipped = Attribute(u'The total quantity that has been shipped '
                    u'already.')
    shippingInfo = Attribute(u'A list of mappings, with fields like: '
                    u'shippingId, shippingDate, quantity, packageId')
    options = Attribute(u'Product options associated with this order item.')

    def remove():
        """ Remove the order item from the order or cart.
        """

    def modify(quantity, **kw):
        """ Change the quantity of the order item (and optionally other
            attributes).
        """

    def setOrder(order):
        """ Assign the order given to the order item.
        """


class IOrderItems(Interface):
    """ A collection of order items.
    """

    def __getitem__(key):
        """ Return the order item identified by the key given.
        """

    def __iter__():
        """ Return an iterator of all order items.
        """

    def query(**criteria):
        """ Search for order items. Possible criteria are:
            product, party, order, run, timeFrom, timeTo.
        """

    def add(product, party, shop, order='???', run=0, quantity=1, **kw):
        """ Create and register an order item; return it. Additional properties
            may be specified via keyword arguments.

            If the order item is already present do not create a new one
            but add the quantity.
        """

    def getCart(party=None, order='???', shop=None, run=0, **kw):
        """ Return a collection of order items.
        """
