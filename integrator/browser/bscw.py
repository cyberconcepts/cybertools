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
BSCW repository view.

$Id$
"""

from datetime import datetime
from time import strptime
from zope.app.pagetemplate import ViewPageTemplateFile
from zope import component
from zope.cachedescriptors.property import Lazy
from zope.traversing.browser import absoluteURL

from cybertools.integrator.base import mimeTypes
from cybertools.integrator.bscw import ContainerFactory, File
from cybertools.integrator.interfaces import IContainerFactory
from cybertools.integrator.interfaces import IItemFactory, IFileFactory


view_macros = ViewPageTemplateFile('view.pt')


class BaseView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def title(self):
        return self.context.title

    @Lazy
    def description(self):
        return self.context.description

    @Lazy
    def modified(self):
        return self.context.modified

    @Lazy
    def url(self):
        return absoluteURL(self.context, self.request)

    @Lazy
    def icon(self):
        return '%s/++resource++%s.png' % (self.request.URL[0], self.context.icon)


class ItemView(BaseView):

    def __init__(self, context, request, parentView):
        super(ItemView, self).__init__(context, request)
        self.parentView = parentView

    @Lazy
    def baseName(self):
        return self.context.icon

    @Lazy
    def url(self):
        if isinstance(self.context, File):
            return self.downloadUrl
        url = self.parentView.url
        return '%s?id=%s' % (url, self.context.internalPath)

    @Lazy
    def downloadUrl(self):
        urlInfo = self.context.externalURLInfo
        baseUrl = urlInfo.baseUrl
        while 'bscw.cgi' in baseUrl and not baseUrl.endswith('bscw.cgi'):
            baseUrl, ignore = baseUrl.rsplit('/', 1)
        if (self.context.contentType == 'application/octet-stream' and
                len(self.title) > 3 and self.title[-4] == '.'):
            extension = ''
        else:
            extensions = mimeTypes.get(self.context.contentType) or ['bin']
            for ext in extensions:
                if self.title.endswith('.' + ext):
                    extension = ''
                    break
            else:
                extension = '.' + extensions[0]
        title = self.title.encode('UTF-8').replace('/', '|')
        return '%s/d%s/%s%s' % (baseUrl, urlInfo.path, title, extension)

    @property
    def breadCrumbs(self):
        parents = [p for p in self.context.parents if p is not None]
        for p in reversed(parents):
            view = ItemView(p, self.request, self.parentView)
            yield dict(url=view.url, title=view.title)
        if parents:
            yield dict(url=self.url, title=self.title)


class BSCWView(BaseView):

    viewTemplate = view_macros
    itemView = ItemView

    @Lazy
    def dataMacro(self):
        return self.viewTemplate.macros['data']

    @Lazy
    def headingMacro(self):
        return self.viewTemplate.macros['heading']

    @Lazy
    def itemMacro(self):
        if self.remoteProxy is None:
            return None
        typeName = self.remoteProxy.itemType.lower()
        return self.viewTemplate.macros.get(typeName, self.defaultMacro)

    @Lazy
    def defaultMacro(self):
        return self.viewTemplate.macros['default']

    @Lazy
    def remoteProxy(self):
        id = self.request.form.get('id')
        proxy = self.context.getProxy(address=id)
        return proxy

    @Lazy
    def item(self):
        if self.remoteProxy is None:
            return None
        return self.itemView(self.remoteProxy, self.request, self)

    def content(self):
        proxy = self.remoteProxy
        for obj in proxy.values():
            yield self.itemView(obj, self.request, self)

