#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
Base classes.

$Id$
"""

from Acquisition import aq_inner, aq_parent
from persistent.mapping import PersistentMapping
from zope.app.container.interfaces import IObjectAddedEvent
from zope import component
from zope.interface import implements

from cybertools.util.generic.interfaces import IGeneric
from cybertools.util.generic.interfaces import IGenericObject, IGenericFolder


_not_found = object()


class GenericObject(object):
    """ A mixin class supporting generic attribute access and other
        basic or common functionality when combined with Zope2's
        SimpleItem.
    """

    implements(IGenericObject)

    typeInterface = None

    def setup(self):
        self.__generic_attributes__ = PersistentMapping()
        if self.typeInterface:
            obj = self.typeInterface(self)
            obj.setup()

    def getGenericAttribute(self, attr, default=_not_found):
        value = self.__generic_attributes__.get(attr, default)
        if value is _not_found:
            raise AttributeError(attr)
        return value

    def setGenericAttribute(self, attr, value):
        self.__generic_attributes__[attr] = value
        return value

    def getParent(self):
        return aq_parent(aq_inner(self))

    def rename(self, newName):
        self.getParent().manage_renameObject(self.name, newName)


class GenericFolder(GenericObject):
    """ Provide generic (i.e. dictionary-like) folder access to Zope2's
        Folder or BTreeFolder.
    """

    implements(IGenericFolder)

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        self._setObject(name, value)

    def getItems(self, types=None):
        return self.objectItems(types)


@component.adapter(IGeneric, IObjectAddedEvent)
def setup(obj, event):
    obj.setup()
component.provideHandler(setup)
