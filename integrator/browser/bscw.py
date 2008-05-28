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


listing_macros = ViewPageTemplateFile('listing.pt')


class BSCWView(object):

    template = listing_macros

    baseUrl = ''
    baseId = ''

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def listing(self):
        return self.template.macros['listing']

    def content(self):
        url = self.context.getRepositoryURL()
        if isinstance(url, basestring):
            server, id = url.rsplit('/', 1)
            self.baseUrl = server
        else:   # already a real server object
            server = url
            id = self.baseId
        id = self.request.form.get('id', id)
        factory = component.getUtility(IContainerFactory, name='bscw')
        root = factory(id, server=server, baseUrl=self.baseUrl)
        return root.values()

    def getUrlForObject(self, obj):
        url = absoluteURL(self.context, self.request)
        return '%s?id=%s' % (url, obj.internalPath)
