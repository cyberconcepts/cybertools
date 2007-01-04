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
from zope.app.traversing.api import traverse, traverseName
from persistent import Persistent as BasePersistent

from cybertools.util.adapter import AdapterFactory


storages = AdapterFactory()


class Adapter(object):

    def __init__(self, context):
        self.context = context
        self.persistent = None

    def save(self, name, path='/'):
        intids = component.getUtility(IIntIds)
        persistent = self.persistent
        if persistent is None:
            persistent = Persistent()
            site = getSite()
            container = traverse(site, path)
            container[name] = persistent
            uid = intids.register(persistent)
        else:
            uid = intids.getId(persistent)
        persistent.update(self.context.__dict__)
        persistent._p_changed = True
        self.persistent = persistent
        return uid

    def load(self, idOrPath):
        if type(idOrPath) is int:
            intids = component.getUtility(IIntIds)
            persistent = intids.getObject(idOrPath)
        else:
            site = getSite()
            persistent = traverse(site, path)
        t = type(self.context)
        class_ = t is type and self.context or t
        obj = self.context = class_()
        obj.__dict__.update(persistent.get())
        return obj

storages.register(Adapter, object)


class Persistent(BasePersistent):

    def update(self, data):
        self.__dict__.update(data)

    def get(self):
        return self.__dict__
