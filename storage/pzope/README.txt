=========================
Zope-based Object Storage
=========================

  ($Id$)

  >>> from zope.app.testing.setup import placefulSetUp, placefulTearDown
  >>> site = placefulSetUp(True)

  >>> from zope import component
  >>> from zope.app.intid.interfaces import IIntIds
  >>> from cybertools.relation.tests import IntIdsStub
  >>> component.provideUtility(IntIdsStub(), IIntIds)

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
  >>> uid = persistent.save('c1')

For loading an object we get a storage adapter to the object's class and
call `load()` on it.

  >>> persistent = storages(Content)
  >>> c2 = persistent.load(uid)
  >>> c2.title
  'changed'


Fin de partie
=============

  >>> placefulTearDown()

