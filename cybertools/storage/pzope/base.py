# cybertools.storage.pzope.base

""" Storage manager implementation for a full Zope 3 environment.
"""

from persistent import Persistent
from zope import component
from zope.interface import implements
from zope.component.hooks import getSite
from zope.container.interfaces import IContained
from zope.intid.interfaces import IIntIds
from zope.traversing.api import traverse, getPath

from cybertools.util.adapter import AdapterFactory


storages = AdapterFactory()


class PersistentObject(Persistent):

    implements(IContained)

    __parent__ = __name__ = None

    def update(self, data):
        self.__dict__.update(data)

    def get(self):
        return self.__dict__


class Adapter(object):

    persistentFactory = PersistentObject

    persistent = address = uid = None

    def __init__(self, context):
        self.context = context

    def save(self, address=None):
        intids = component.getUtility(IIntIds)
        persistent = self.persistent
        if persistent is None:
            if self.address is None:
                self.address = address
            else:
                address = self.address
            path, name = address.rsplit('/', 1)
            container = traverse(getSite(), path + '/')
            if name in container:
                persistent = container[name]
                uid = intids.getId(persistent)
            else:
                persistent = self.persistentFactory()
                container[name] = persistent
                uid = intids.register(persistent)
        else:
            uid = intids.getId(persistent)
        persistent.update(self.context.__dict__)
        persistent._p_changed = True
        self.persistent = persistent
        self.uid = uid
        return uid

    def load(self, address=None):
        intids = component.getUtility(IIntIds)
        if self.uid is not None:  # if ever possible we use the intId
            address = self.uid
        if type(address) is int:  # seems to be an intId
            persistent = intids.getObject(address)
            self.address = getPath(persistent)
        else:
            if self.address is None:
                self.address = address
            else:
                address = self.address
            persistent = traverse(getSite(), address)
            self.uid = intids.register(persistent)
        t = type(self.context)
        factory = t is type and self.context or t
        obj = self.context = factory()
        obj.__dict__.update(persistent.get())
        self.persistent = persistent
        return obj

storages.register(Adapter, object)

