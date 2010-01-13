============================================
General-purpose Link and Relation Management
============================================

  ($Id$)

Basic setup
-----------

  >>> from zope import component
  >>> from cybertools.link.tests import IntIdsStub
  >>> intids = IntIdsStub()
  >>> component.provideUtility(intids)

  >>> from cybertools.link.base import LinkManager
  >>> links = LinkManager()

Create and link objects
-----------------------

We create a simple class to derive objects from it.

  >>> class Page(object):
  ...     pass

  >>> p1 = Page()
  >>> p2 = Page()

These objects have to be registered with the IntIds utility.

  >>> intids.register(p1)
  0
  >>> intids.register(p2)
  1

Now we can create a link from p1 to p2.
Usually the link gets a name that is related to the target.

  >>> l01 = links.createLink(name='p2', source=p1, target=p2)

Let's have a look at the newly created link and the default values of some
of its attributes.

  >>> (l01.identifier, l01.source, l01.target, l01.name, l01.linkType, l01.state,
  ...  l01.relevance, l01.order)
  (1, 0, 1, 'p2', u'link', u'valid', 1.0, 0)

Query for links
---------------

We are now able to query the link manager for links, e.g. using name and
source for finding all corresponding links on a page.

  >>> [l.identifier for l in links.query(name='p2', source=p1)]
  [1]
