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

from zope.app.pagetemplate import ViewPageTemplateFile
from zope import component
from zope.cachedescriptors.property import Lazy
from zope.traversing.browser import absoluteURL

from cybertools.integrator.bscw import ContainerFactory
from cybertools.integrator.interfaces import IContainerFactory


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
    def url(self):
        url = self.parentView.url
        return '%s?id=%s' % (url, self.context.internalPath)


class BSCWView(BaseView):

    viewTemplate = view_macros
    itemView = ItemView

    baseUrl = ''
    baseId = ''

    @Lazy
    def listing(self):
        return self.viewTemplate.macros['listing']

    @Lazy
    def heading(self):
        return self.viewTemplate.macros['heading']

    @Lazy
    def remoteProxy(self):
        url = self.context.getRepositoryURL()
        if isinstance(url, basestring):
            server, id = url.rsplit('/', 1)
            self.baseUrl = server
        else:   # already a real server object
            server = url
            id = self.baseId
        id = self.request.form.get('id', id)
        factory = component.getUtility(IContainerFactory, name='bscw')
        return factory(id, server=server, baseUrl=self.baseUrl)

    @Lazy
    def item(self):
        return self.itemView(self.remoteProxy, self.request, self)

    def content(self):
        proxy = self.remoteProxy
        for obj in proxy.values():
            yield self.itemView(obj, self.request, self)

    #def getUrlForObject(self, obj):
    #    url = absoluteURL(self.context, self.request)
    #    return '%s?id=%s' % (url, obj.internalPath)
