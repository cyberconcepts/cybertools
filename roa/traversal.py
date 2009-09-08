#
#  Copyright (c) 2009 Helmut Merz - helmutm@cy55.de
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
IPublishTraverse adapter that checks the 'Accept' header.

$Id$
"""

from zope.app.container.traversal import ItemTraverser
from zope import component


jsonMimeTypes = ('application/json',)


def isJSONRequest(request):
    return request.get('HTTP_ACCEPT').split(';', 1)[0] in jsonMimeTypes
    #return request.get('CONTENT_TYPE') in jsonMimeTypes


class CheckJSONTraverser(ItemTraverser):

    def getChild(self, name):
        # may be overwritten by subclass
        return self.context.get(name)

    def publishTraverse(self, request, name):
        if isJSONRequest(request):
            return self.jsonTraverse(request, name)
        return self.defaultTraverse(request, name)

    def jsonTraverse(self, request, name):
        method = self.request['REQUEST_METHOD']
        child = self.getChild(name)
        print '*** traversing', method, self.context, name, child
        if self.getTraversalStack():
            if child is None:
                raise AttributeError(name)
            return child
        if child is None:
            if method == 'PUT':
                view = component.getMultiAdapter((self.context, request), name='json')
                return view.create(name)
            raise AttributeError(name)
        view = component.getMultiAdapter((child, request), name='json')
        if method == 'PUT':
            return view.put()
        return view.get()

    def defaultTraverse(self, request, name):
        return super(CheckJSONTraverser, self).publishTraverse(request, name)

    def browserDefault(self, request):
        if self.isJSONRequest(request):
            return self.context, ('@@json',)
        return super(CheckJSONTraverser, self).browserDefault(request)

    def getTraversalStack(self):
        return self.request['TraversalRequestNameStack']
