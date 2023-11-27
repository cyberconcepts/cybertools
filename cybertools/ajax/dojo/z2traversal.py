#
#  Copyright (c) 2008 Helmut Merz - helmutm@cy55.de
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
Customized IPublishTraverse adapter(s) for Zope 2.

$Id$
"""

from zope.publisher.interfaces import NotFound


class ResourceTraverser(object):
    """ IPublishTraverse adapter for file and directory resources,
        allows using resource file names with underscores, like e.g.
        used by Dojo.

        Include in your configure.zcml via this directive:
          <zope:adapter
                for="zope.component.interfaces.IResource
                     zope.publisher.interfaces.browser.IBrowserRequest"
                provides="zope.publisher.interfaces.browser.IBrowserPublisher"
                factory="cybertools.ajax.dojo.z2traversal.ResourceTraverser" />
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        if hasattr(self.context, 'get'):
            subob = self.context.get(name, None)
        else:
            subob = getattr(self.context, name, None)
        if subob is None:
            raise NotFound(self.context, name, request)
        return subob

    def browserDefault(self, request):
        if hasattr(self.context, '__browser_default__'):
            return self.context.__browser_default__(request)
        return self.context, ()
