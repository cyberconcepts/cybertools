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
Access to objects in a BSCW repository.

$Id$
"""

import os
from datetime import datetime
from time import strptime
from xmlrpclib import ServerProxy
from zope import component
from zope.app.file.image import getImageInfo
from zope.cachedescriptors.property import Lazy
from zope.contenttype import guess_content_type
from zope.interface import implements, Attribute

from cybertools.integrator.base import ContainerFactory, ItemFactory, FileFactory
from cybertools.integrator.base import ReadContainer, Item, File, Image
from cybertools.integrator.base import ExternalURLInfo
from cybertools.integrator.interfaces import IContainerFactory
from cybertools.integrator.interfaces import IItemFactory, IFileFactory


baseAttributes = ['__class__', 'name', 'id', 'descr', 'notes',
    'bound_sub_artifacts', 'creator', 'owner', 'owners',
    'ctime', 'mtime', 'atime', 'lastEvent', 'createEvent',
    'lastChange', 'lastMove', 'containers', 'access']

minimalAttributes = ['__class__', 'name', 'id', 'descr', 'mtime']

additionalAttributes = ['banner', 'moderated', 'ratings']

documentAttributes = ['vid', 'vstore', 'file_extensions', 'size', 'encoding', 'type']

urlAttributes = ['url_link', 'last_verified', 'last_error', 'content_length',
    'content_type', 'content_encoding', 'last_modified']

standardAttributes = ['__class__', 'type', 'id', 'name', 'descr',
            'ctime', 'mtime', 'creator', 'owner', 'owner',
            'url_link', 'size', 'encoding']

classes = ['cl_core.Folder', 'cl_core.Document', 'cl_core.URL', ]


class BSCWConnection(object):

    factoryName = 'bscw'

    baseURL = rootId = ''

    def __init__(self, url, server=None):
        self.repositoryURL = url
        self.setURLs()
        if server is None:
            server = ServerProxy(self.baseURL())
        self.server = server

    def getRepositoryURL(self):
        return self.repositoryURL

    def setURLs(self):
        url = self.getRepositoryURL()
        if url:
            self.baseURL, self.rootId = url.rsplit('/', 1)

    def getItem(self, address):
        return self.server.get_attributes(address, standardAttributes, 1, True)

    def getProxy(self, item=None, address=None, parentPath=''):
        if item is None:
            if address is None:
                address = self.rootId
            item = self.getItem(address)[0]
        address = item['id']
        itemType = item['__class__'].split('.')[-1]
        internalPath = '/'.join((parentPath, address)).strip('/')
        params = dict(connection=self, internalPath=internalPath,
                      properties=item, baseURL=self.baseURL,
                      itemType=itemType)
        if itemType == 'Folder':
            return self.containerFactory(address, **params)
        elif itemType == 'Document':
            return self.fileFactory(address, contentType=item['type'],
                                    **params)
        else:
            return self.itemFactory(address, **params)

    @Lazy
    def itemFactory(self):
        return component.getUtility(IItemFactory, name=self.factoryName)

    @Lazy
    def fileFactory(self):
        return component.getUtility(IFileFactory, name=self.factoryName)

    @Lazy
    def containerFactory(self):
        return component.getUtility(IContainerFactory, name=self.factoryName)


# proxy classes

class BSCWProxyBase(object):

    @Lazy
    def externalURLInfo(self):
        id = self.address
        if id.startswith('bs_'):
            id = id[3:]
        return ExternalURLInfo(self.baseURL, id)

    @Lazy
    def attributes(self):
        return self.connection.getItem(self.address)

    @Lazy
    def properties(self):
        return self.attributes[0]

    @Lazy
    def title(self):
        return self.properties['name']

    @Lazy
    def description(self):
        return self.properties.get('descr', u'')

    @Lazy
    def modified(self):
        dt = self.properties['mtime']
        return dt and datetime(*(strptime(str(dt), '%Y%m%dT%H:%M:%SZ')[0:6])) or ''


class ReadContainer(BSCWProxyBase, ReadContainer):

    factoryName = 'bscw'

    @Lazy
    def data(self):
        data = self.attributes
        if len(data) > 1:
            return dict((item['id'], item) for item in data[1])
        else:
            return {}

    def keys(self):
        return self.data.keys()

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        raise KeyError(key)

    def get(self, key, default=None):
        if key not in self.data:
            return default
        item = self.data[key]
        return self.connection.getProxy(item)

    def values(self):
        return sorted((self.get(k) for k in self),
                      key=lambda x: x.title.lower())


    def __len__(self):
        return len(self.keys())

    def items(self):
        return [(k, self.get(k)) for k in self]

    def __contains__(self, key):
        return key in self.keys()


class Item(BSCWProxyBase, Item):

    @property
    def icon(self):
        return self.itemType.lower()

    @Lazy
    def type(self):
        return 'unknown'


class File(BSCWProxyBase, File):

    contentType = None

    def getData(self, num=None):
        return self.server.get_document()
    data = property(getData)

    def getSize(self):
        return 0


class Image(File, Image):

    pass


# factory classes

class ContainerFactory(ContainerFactory):

    proxyClass = ReadContainer


class ItemFactory(ItemFactory):

    proxyClass = Item


class FileFactory(FileFactory):

    def __call__(self, address, **kw):
        contentType = kw.pop('contentType', 'application/octet-stream')
        if contentType.startswith('image/'):
            obj = Image(address, contentType, **kw)
        else:
            obj = File(address, contentType, **kw)
        obj.contentType = contentType
        return obj
