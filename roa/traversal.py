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


class CheckJSONTraverser(ItemTraverser):

    def publishTraverse(self, request, name):
        if self.isJSONRequest(request):
            return self.jsonTraverse(request, name)
        return self.defaultTraverse(request, name)

    def isJSONRequest(self, request):
        return request.get('CONTENT_TYPE') in jsonMimeTypes

    def jsonTraverse(self, request, name):
        item = self.context.get(name)
        if item is not None:
            return item
        # TODO: specify provides=IJSONView
        view = component.getMultiAdapter((self.context, request), name='json')
        if view is None:
            return self.defaultTraverse(request, name)
        return view.traverse(name)

    def defaultTraverse(self, request, name):
        return super(CheckAcceptTraverser, self).publishTraverse(request, name)
