=========================
Zope-based Object Storage
=========================

  ($Id$)

  >>> from zope.app.testing.setup import placefulSetUp, placefulTearDown
  >>> site = placefulSetUp(True)

As the Zope-based storage keeps track of the objects using unique ids
we need a utility that provides these. For testing we use a dummy
implementation; the real stuff is in zope.app.intids and there must
be a corresponding utility in the root site folder of your Zope.

  >>> from zope import component
  >>> from cybertools.relation.tests import IntIdsStub
  >>> component.provideUtility(IntIdsStub())

We first need a class from which we will create objects that later on
will be stored in and retrieved from the storage.

  >>> class Content(object):
  ...     title = 'demo'

  >>> c1 = Content()
  >>> c1.title
  'demo'
  >>> c1.title = 'changed'
  >>> c1.title
  'changed'

We can save the object in the storage by getting a storage adapter
from the corresponding factory in the `manager` module and calling
`save()` on it.

  >>> from cybertools.storage.pzope.manager import storages
  >>> persistent = storages(c1)
  >>> c1Uid = persistent.save('c1')

For loading an object we get a storage adapter to the object's class and
call `load()` on it, providing the UID we had got back when saving the
object.

  >>> persistent = storages(Content)
  >>> c2 = persistent.load(c1Uid)
  >>> c2.title
  'changed'


Fin de partie
=============

  >>> placefulTearDown()

