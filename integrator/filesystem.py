#
#  Copyright (c) 2012 Helmut Merz helmutm@cy55.de
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
Access to objects in the file system.
"""

import os, stat

from zope import component
from zope.app.file.image import getImageInfo
from zope.cachedescriptors.property import Lazy
from zope.contenttype import guess_content_type
from zope.interface import implements, Attribute

from cybertools.integrator.base import ContainerFactory, FileFactory
from cybertools.integrator.base import ReadContainer, File, Image


# proxy classes

class ReadContainer(ReadContainer):

    factoryName = 'filesystem'

    @property
    def filenames(self):
        return os.listdir(self.address)

    def keys(self):
        return [n for n in self.filenames if not n.startswith('.')]

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        raise KeyError(key)

    def get(self, key, default=None):
        if key not in self.keys():
            return default
        path = os.path.join(self.address, key)
        internalPath = '/'.join((self.internalPath, key)).strip('/')
        if os.path.isdir(path):
            return self.containerFactory(path, internalPath=internalPath,
                            __parent__=self.__parent__)
        else:
            return self.fileFactory(path, internalPath=internalPath,
                            __parent__=self.__parent__)

    def values(self):
        return [self.get(k) for k in self]

    def __len__(self):
        return len(self.keys())

    def items(self):
        return [(k, self.get(k)) for k in self]

    def __contains__(self, key):
        return key in self.keys()


class File(File):

    contentType = None
    data = None

    def getData(self, num=-1):
        f = open(self.address, 'r')
        data = f.read(num)
        f.close()
        return data

    data = property(getData)

    def getSize(self):
        return os.stat(self.address)[stat.ST_SIZE]


class Image(File):

    width = height = 0
    icon = 'image'

    def getImageSize(self):
        return self.width, self.height


# factory classes

class ContainerFactory(ContainerFactory):

    proxyClass = ReadContainer


class FileFactory(FileFactory):

    proxyClass = File
    imageClass = Image

    def __call__(self, address, **kw):
        contentType = kw.pop('contentType', None)
        width = height = 0
        obj = self.proxyClass(address, contentType, **kw)
        if not contentType:
            data = obj.getData(50)
            contentType, width, height = getImageInfo(data)
        if not contentType:
            name = os.path.basename(address)
            contentType, encoding = guess_content_type(name, data, '')
        if contentType.startswith('image/'):
            return self.imageClass(address, contentType=contentType,
                         width=width, height=height, **kw)
        else:
            obj.contentType = contentType
            return obj
