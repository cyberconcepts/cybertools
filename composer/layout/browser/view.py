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
Basic view classes for layout-based presentation.

$Id$
"""

from zope import component
from zope.interface import Interface, implements
from zope.cachedescriptors.property import Lazy
from zope.app.pagetemplate import ViewPageTemplateFile

from cybertools.composer.layout.interfaces import ILayoutManager


class BaseView(object):

    template = ViewPageTemplateFile('base.pt')

    def __init__(self, context, request, name=None):
        self.context = self.__parent__ = context
        self.request = request
        if name is not None:
            self.name = name

    def update(self):
        return True

    def __call__(self):
        return self.template(self)


class LayoutView(BaseView):

    name = 'base'

    @Lazy
    def renderer(self):
        return self.context.renderer

    @Lazy
    def layouts(self):
        return ViewLayouts(self)

    @Lazy
    def resources(self):
        return ViewResources(self)

    def getRegion(self, key):
        manager = component.getUtility(ILayoutManager)
        return manager.regions.get('.'.join((self.name, key)))


class Page(LayoutView):

    name = 'page'

    #@Lazy
    def body(self):
        return self.layouts['body'][0]()


class ViewLayouts(object):

    def __init__(self, view):
        self.view = view

    def __getitem__(self, key):
        view = self.view
        region = view.getRegion(key)
        if region is None:
            return []
        return [LayoutView(layout, view.request, name=key)
                for layout in region.layouts]


class ViewResources(object):

    def __init__(self, view):
        self.view = view

    def __getitem__(self, key):
        return []
