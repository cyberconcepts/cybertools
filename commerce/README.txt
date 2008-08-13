=================================================
Commerce: Shope, Products, Customers, Orders, ...
=================================================

  ($Id$)


Shops and Products
==================

Let's start with a Shop:

  >>> from cybertools.commerce.base import Shop
  >>> shop1 = Shop(u'shop1', u'PC up Ltd')

Now we add products to the shop.

  >>> from cybertools.commerce.product import Product
  >>> p001 = Product(u'p001', u'Silent Case')

  >>> shop1.products.add(p001)

  >>> sorted((name, p.title) for name, p in shop1.products.items())
  [(u'p001', u'Silent Case')]

Let's have a look at the product - it should correctly reference the shop
it belongs to.

  >>> len(p001.shops)
  1
  >>> p001.shops.keys()[0]
  u'shop1'


Customers
=========

  >>> from cybertools.commerce.customer import Customer
  >>> c001 = Customer(u'c001', u'Your Local Store')


Orders
======

