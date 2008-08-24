=================================================
Commerce: Shope, Products, Customers, Orders, ...
=================================================

  ($Id$)


Shops and Products
==================

Let's start with two shops:

  >>> from cybertools.commerce.shop import Shop
  >>> shop1 = Shop(u'shop1', u'PC up Ltd')
  >>> shop2 = Shop(u'shop2', u'Video up Ltd')

Now we add products to the shops.

  >>> from cybertools.commerce.product import Product
  >>> p001 = Product(u'001', u'Silent Case')
  >>> p002 = Product(u'002', u'Portable Projector')
  >>> p003 = Product(u'003', u'HD Flatscreen Monitor')
  >>> p004 = Product(u'004', u'Giga Mainboard')

  >>> shop1.products.add(p001)
  >>> shop1.products.add(p003)
  >>> shop1.products.add(p004)
  >>> shop2.products.add(p002)
  >>> shop2.products.add(p003)

  >>> sorted((p.productId, p.title) for p in shop1.products)
  [(u'001', u'Silent Case'), (u'003', u'HD Flatscreen Monitor'),
   (u'004', u'Giga Mainboard')]

Let's have a look at the product - it should correctly reference the shops
it belongs to.

  >>> sorted((s.name, s.title) for s in p003.shops)
  [(u'shop1', u'PC up Ltd'), (u'shop2', u'Video up Ltd')]


Customers
=========

  >>> from cybertools.commerce.customer import Customer
  >>> c001 = Customer(u'001', u'Your Local Computer Store')
  >>> c002 = Customer(u'002', u'Speedy Gonzales')
  >>> c003 = Customer(u'003', u'TeeVee')
  >>> c004 = Customer(u'004', u'MacVideo')

  >>> shop1.customers.add(c001)
  >>> shop1.customers.add(c002)
  >>> shop1.customers.add(c004)
  >>> shop2.customers.add(c002)
  >>> shop2.customers.add(c003)
  >>> shop2.customers.add(c004)

  >>> sorted((c.customerId, c.title) for c in shop1.customers)
  [(u'001', u'Your Local Computer Store'), (u'002', u'Speedy Gonzales'),
   (u'004', u'MacVideo')]

  >>> sorted((s.name, s.title) for s in c002.shops)
  [(u'shop1', u'PC up Ltd'), (u'shop2', u'Video up Ltd')]


Orders
======

