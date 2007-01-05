#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
Storage manager implementation for a full Zope 3 environment.

$Id$
"""

from zope import component
from zope.interface import implements
from zope.app.component.hooks import getSite
from zope.app.container.interfaces import IContained
from zope.app.intid.interfaces import IIntIds
from zope.app.traversing.api import traverse, getPath
from persistent import Persistent

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
                self.address = address  # lets
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

