#
#  Copyright (c) 2005 Helmut Merz helmutm@cy55.de
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
cybertools regions.

$Id$
"""

from zope.interface import implements
import zope.component
from zope.app.publisher.interfaces.browser import IBrowserView
from zope.app.publisher.browser import BrowserView
from zope.contentprovider.interfaces import IContentProvider
from zope.viewlet.manager import ViewletManagerBase


class BaseView(object):
    """ Basic view class using a template and possibly doing some other
        setup stuff.
    """

    implements(IBrowserView)

    def __call__(self):
        # render the template associated with this view:
        return self.index()
    

class PageProviderView(object):
    """ Simple view class using a content provider for setting up a page.
    """

    implements(IBrowserView)

    def __call__(self):
        context = self.context
        request = self.request
        name = 'cybertools.pageprovider'
        provider = zope.component.queryMultiAdapter(
            (context, request, self), IContentProvider, name)
        provider.update()
        return provider.render()


class PageProvider(ViewletManagerBase):
    """ Simple implementation that provides a whole page.
    """

    implements(IContentProvider)

    def __init__(self, context, request, view):
        self.context = context
        self. request = request
        self.view = view
        self.__parent__ = view

    def update(self):
        return ViewletManagerBase.update(self)

    def render(self):
        return ViewletManagerBase.render(self)
