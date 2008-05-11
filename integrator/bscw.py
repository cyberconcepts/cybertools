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
from xmlrpclib import ServerProxy
from zope import component
from zope.app.file.image import getImageInfo
from zope.cachedescriptors.property import Lazy
from zope.contenttype import guess_content_type
from zope.interface import implements, Attribute

from cybertools.integrator.base import ContainerFactory, FileFactory
from cybertools.integrator.base import ReadContainer, File, Image
from cybertools.text import mimetypes


baseAttributes = ['__class__', 'name', 'id', 'descr', 'notes',
    'bound_sub_artifacts', 'creator', 'owner', 'owners',
    'ctime', 'mtime', 'atime', 'lastEvent', 'createEvent',
    'lastChange', 'lastMove', 'containers', 'access']

standardAttributes = ['__class__', 'name', 'id', 'descr', 'mtime']

additionalAttributes = ['banner', 'moderated', 'ratings']

documentAttributes = ['vid', 'vstore', 'file_extensions', 'size', 'encoding', 'type']

urlAttributes = ['url_link', 'last_verified', 'last_error', 'content_length',
    'content_type', 'content_encoding', 'last_modified']

classes = ['cl_core.Folder', 'cl_core.Document', 'cl_core.URL', ]


# proxy classes

class ReadContainer(ReadContainer):

    factoryName = 'bscw'

    @Lazy
    def data(self):
        data = self.server.get_attributes(self.address,
                ['__class__', 'type', 'id', 'name', 'descr', 'url_link'], 1, True)
        return dict((item['id'], item) for item in data[1])

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
        if 'Folder' in item['__class__']:
            return self.containerFactory(item['id'], server=self.server,
                                         name=item['name'])
        elif 'Document' in item['__class__']:
            return self.fileFactory(item['id'], item['type'], server=self.server,
                                    name=item['name'])
        else:
            return OtherObject(item['id'], None, server=self.server, name=item['name'])

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

    def getData(self):
        return self.server.get_document()
    data = property(getData)

    def getSize(self):
        return 0


class OtherObject(File):

    data = u''


# factory classes

class ContainerFactory(ContainerFactory):

    proxyClass = ReadContainer

    def __call__(self, address, **kw):
        server = kw.pop('server')
        if isinstance(server, basestring):  # just a URL, resolve for XML-RPC
            server = ServerProxy(server)
        return self.proxyClass(address, server=server, **kw)


class FileFactory(FileFactory):

    def __call__(self, address, **kw):
        contentType = kw.pop('type', 'application/octet-stream')
        obj = File(address, contentType, **kw)
        obj.contentType = contentType
        return obj
