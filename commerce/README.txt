=================================================
Commerce: Shope, Products, Customers, Orders, ...
=================================================

  ($Id$)

  >>> from zope import component

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

We can also create a manufacturer and set it for a product.

  >>> mf001 = manager.manufacturers.create(u'001', title=u'Global Electronics')
  >>> p001.manufacturer = mf001
  >>> [p.title for p in mf001.products]
  [u'Silent Case']


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


Carts and Orders
================

A cart is just a collection of order items belonging to a certain customer
(or some other kind of party).

  >>> orderItems = manager.orderItems

  >>> orderItems.add(p001, c001, shop=shop1, quantity=3)
  <OrderItem [2, 1, 7, '... ...', '???']: {'shop': 0, 'quantity': 3}>

  >>> orderItems.getCart(c001)
  [<OrderItem [2, 1, 7, '... ...', '???']: {'shop': 0, 'quantity': 3}>]

Orders
------

The items in a shopping cart may be included in an order.

  >>> ord001 = manager.orders.create(u'001', shop=shop1, customer=c001)

  >>> for item in orderItems.getCart(c001):
  ...     item.setOrder(ord001)

Now the default cart is empty; we have to supply the order for
retrieving the order items.

  >>> orderItems.getCart(c001)
  []
  >>> orderItems.getCart(c001, ord001)
  [<OrderItem [2, 1, 7, '... ...', 11]: {'shop': 0, 'quantity': 3}>]
