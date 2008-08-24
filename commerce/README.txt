=================================================
Commerce: Shope, Products, Customers, Orders, ...
=================================================

  ($Id$)

  >>> from cybertools.commerce.manager import Manager
  >>> manager = Manager()


Shops and Products
==================

Let's start with two shops:

  >>> shop1 = manager.shops.create(u'shop1', title=u'PC up Ltd')
  >>> shop2 = manager.shops.create(u'shop2', title=u'Video up Ltd')

  >>> len(list(manager.shops))
  2

Now we add products to the shops.

  >>> p001 = manager.products.create(u'001', title=u'Silent Case')
  >>> p002 = manager.products.create(u'002', title=u'Portable Projector')
  >>> p003 = manager.products.create(u'003', title=u'HD Flatscreen Monitor')
  >>> p004 = manager.products.create(u'004', title=u'Giga Mainboard')

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

  >>> c001 = manager.customers.create(u'001', title=u'Your Local Computer Store')
  >>> c002 = manager.customers.create(u'002', title=u'Speedy Gonzales')
  >>> c003 = manager.customers.create(u'003', title=u'TeeVee')
  >>> c004 = manager.customers.create(u'004', title=u'MacVideo')

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

