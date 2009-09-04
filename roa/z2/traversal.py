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
IPublishTraverse adapter for Zope 2 that checks the 'Accept' header.

$Id$
"""

from ZPublisher.BaseRequest import DefaultPublishTraverse
from ZPublisher.HTTPRequest import HTTPRequest

from cybertools.roa.traversal import CheckJSONTraverser as BaseTraverser
from cybertools.roa.traversal import isJSONRequest


class CheckJSONTraverser(BaseTraverser, DefaultPublishTraverse):

    defaultTraverse = DefaultPublishTraverse.publishTraverse

    def browserDefault(self, request):
        if isJSONRequest(request):
            return self.context, ('@@json',)
        return DefaultPublishTraverse.browserDefault(self, request)


old_traverse = HTTPRequest.traverse

def traverse(self, *args, **kw):
    if isJSONRequest(self):
        self.maybe_webdav_client = 0
    old_traverse(self, *args, **kw)

HTTPRequest.traverse = traverse

print '***** HTTPRequest.traverse monkey patch installed.'
