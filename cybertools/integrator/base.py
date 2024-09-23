# cybertools.util.integrator.base

""" Base implementation for accessing external content objects.
"""

import mimetypes
import os
from urllib.parse import urlencode
from zope.container.contained import Contained
from zope.cachedescriptors.property import Lazy
from zope import component
from zope.interface import implementer

from cybertools.integrator.interfaces import IContainerFactory
from cybertools.integrator.interfaces import IItemFactory, IFileFactory
from cybertools.integrator.interfaces import IReadContainer, IItem, IFile, IImage


# proxy base (sample) classes

class ProxyBase(object):

    __parent__ = None
    factoryName = 'sample'

    internalPath = ''
    externalUrlInfo = None

    description = u''
    authors = ()
    created = modified = None

    def __init__(self, address, **kw):
        self.address = address
        for k, v in kw.items():
            setattr(self, k, v)

    @Lazy
    def title(self):
        if self.internalPath:
            return self.internalPath.rsplit('/', 1)[-1]
        return self.address.rsplit(os.path.sep, 1)[-1]


@implementer(IReadContainer)
class ReadContainer(ProxyBase, Contained):

    icon = 'folder'

    @Lazy
    def properties(self):
        return {}

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


@implementer(IItem)
class Item(ProxyBase, object):

    icon = 'item'
    __parent__ = None


@implementer(IFile)
class File(Item):

    def __init__(self, address, contentType, **kw):
        super(File, self).__init__(address, **kw)
        self.contentType = contentType

    def getData(self, num=None):
        return ''

    data = property(getData)

    def getSize(self):
        return len(self.data)

    @property
    def icon(self):
        return (mimeTypes.get(self.contentType) or ['unknown'])[0]


@implementer(IImage)
class Image(File):

    icon = 'image'

    def getImageSize(self):
        return 0, 0


# URL info

class ExternalURLInfo(object):

    def __init__(self, baseUrl='', path='', params=None):
        self.baseUrl, self.path = baseUrl.strip('/'), path.strip('/')
        self.params = params or {}

    def __str__(self):
        params = self.params and ('?' + urlencode(self.params)) or ''
        return '%s/%s%s' % (self.baseUrl, self.path, params)


# factory base (sample) classes

class Factory(object):

    proxyClass = ReadContainer

    def __call__(self, address, **kw):
        return self.proxyClass(address, **kw)


@implementer(IContainerFactory)
class ContainerFactory(Factory):

    proxyClass = ReadContainer


@implementer(IItemFactory)
class ItemFactory(Factory):

    proxyClass = Item


@implementer(IFileFactory)
class FileFactory(Factory):

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
                self[parts[0].strip()] = parts[1:]
        mtFile.close()

mimeTypes = MimeTypes()


mimetypes.init([os.path.join(os.path.dirname(__file__), 'mime.types')] +
               mimetypes.knownfiles)
