# cybertools.z2.generic

""" Base classes.
"""

from Acquisition import aq_inner, aq_parent
from persistent.mapping import PersistentMapping
from zope.app.container.interfaces import IObjectAddedEvent
from zope import component
from zope.interface import implementer

from cybertools.util.generic.interfaces import IGeneric
from cybertools.util.generic.interfaces import IGenericObject, IGenericFolder


_not_found = object()


@implementer(IGenericObject)
class GenericObject(object):
    """ A mixin class supporting generic attribute access and other
        basic or common functionality when combined with Zope2's
        SimpleItem.
    """

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


@implementer(IGenericFolder)
class GenericFolder(GenericObject):
    """ Provide generic (i.e. dictionary-like) folder access to Zope2's
        Folder or BTreeFolder.
    """

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        self._setObject(name, value)

    def getItems(self, types=None):
        return self.objectItems(types)

    def values(self, types=None):
        return self.objectValues(types)


@component.adapter(IGeneric, IObjectAddedEvent)
def setup(obj, event):
    obj.setup()
component.provideHandler(setup)
