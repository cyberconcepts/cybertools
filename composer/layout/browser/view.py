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

from cybertools.composer.layout.base import Layout, LayoutInstance
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


class Page(BaseView):

    def __call__(self):
        layout = Layout()
        layout.renderer = ViewPageTemplateFile('main.pt').macros['page']
        instance = LayoutInstance(self.context)
        instance.template = layout
        view = LayoutView(instance, self.request, name='page')
        view.body = view.layouts['body'][0]
        return view.template(view)


class LayoutView(BaseView):

    name = 'base'

    @Lazy
    def client(self):
        return self.context.context

    @Lazy
    def renderer(self):
        renderer = self.context.renderer
        if renderer is None:
            raise ValueError('No renderer found for %r.' % self.context)
        return renderer

    @Lazy
    def layouts(self):
        return ViewLayouts(self)

    @Lazy
    def resources(self):
        return ViewResources(self)

    def getRegion(self, key):
        manager = component.getUtility(ILayoutManager)
        return manager.regions.get('.'.join((self.name, key)))


# subview providers

class ViewLayouts(object):

    def __init__(self, view):
        self.view = view

    def __getitem__(self, key):
        view = self.view
        region = view.getRegion(key)
        if region is None:
            return []
        subviews = []
        for layout in region.layouts:
            instance = LayoutInstance(view.client)
            instance.template = layout
            instance.view = view
            subviews.append(LayoutView(instance, view.request, name=key))
        return subviews


class ViewResources(object):

    def __init__(self, view):
        self.view = view

    def __getitem__(self, key):
        print key
        # TODO...
        return []
