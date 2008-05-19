#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
Base implementation for accessing external content objects.

$Id$
"""

import os
from zope.app.container.contained import Contained
from zope.cachedescriptors.property import Lazy
from zope import component
from zope.interface import implements

from cybertools.integrator.interfaces import IContainerFactory
from cybertools.integrator.interfaces import IItemFactory, IFileFactory
from cybertools.integrator.interfaces import IReadContainer, IItem, IFile, IImage


# proxy base (sample) classes

class ReadContainer(Contained):

    implements(IReadContainer)

    __parent__ = None
    factoryName = 'sample'

    icon = 'folder'

    def __init__(self, address, **kw):
        self.address = address
        for k, v in kw.items():
            setattr(self, k, v)

    @Lazy
    def itemFactory(self):
        return component.getUtility(IItemFactory, name=self.factoryName)

    @Lazy
    def fileFactory(self):
        return component.getUtility(IFileFactory, name=self.factoryName)

    @Lazy
    def containerFactory(self):
        return component.getUtility(IContainerFactory, name=self.factoryName)

    def keys(self):
        return [k for k, v in self.items()]

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        raise KeyError(key)

    def get(self, key, default=None):
        return default

    def values(self):
        return [v for k, v in self.items()]

    def __len__(self):
        return len(self.keys())

    def items(self):
        return []

    def __contains__(self, key):
        return key in self.keys()

    has_key = __contains__


class Item(object):

    implements(IItem)

    contentType = None
    icon = 'item'
    __parent__ = None

    def __init__(self, address, **kw):
        self.address = address
        for k, v in kw.items():
            setattr(self, k, v)


class File(Item):

    implements(IFile)

    def __init__(self, address, contentType, **kw):
        self.address = address
        self.contentType = contentType
        for k, v in kw.items():
            setattr(self, k, v)

    def getData(self, num=None):
        return ''

    data = property(getData)

    def getSize(self):
        return len(self.data)

    @property
    def icon(self):
        return (mimeTypes.get(self.contentType) or ['unknown'])[0]


class Image(File):

    implements(IImage)

    icon = 'image'

    def getImageSize(self):
        return 0, 0


# factory base (sample) classes

class Factory(object):

    proxyClass = ReadContainer

    def __call__(self, address, **kw):
        return self.proxyClass(address, **kw)


class ContainerFactory(Factory):

    implements(IContainerFactory)

    proxyClass = ReadContainer


class ItemFactory(Factory):

    implements(IItemFactory)

    proxyClass = Item


class FileFactory(Factory):

    implements(IFileFactory)

    proxyClass = File   # real implementations should also care about images


# provide a dictionary of MIME types with extensions = icon names

class MimeTypes(dict):

    def __init__(self):
        super(MimeTypes, self).__init__()
        fn = os.path.join(os.path.dirname(__file__), 'mime.types')
        mtFile = open(fn, 'r')
        for line in mtFile:
            line = line.strip()
            if line:
                parts = line.split()
                self[parts[0]] = parts[1:]
        mtFile.close()

mimeTypes = MimeTypes()
