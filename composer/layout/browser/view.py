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

from cybertools.composer.layout.base import Layout
from cybertools.composer.layout.interfaces import ILayoutManager, ILayoutInstance


class BaseView(object):

    template = ViewPageTemplateFile('base.pt')

    page = None
    parent = None
    skin = None

    def __init__(self, context, request, **kw):
        self.context = self.__parent__ = context
        self.request = request
        for k, v in kw.items():
            setattr(self, k, v)

    def __call__(self):
        return self.template(self)

    def update(self):
        return True


class Page(BaseView):

    macroName = 'page'

    @Lazy
    def rootView(self):
        return self

    def __call__(self):
        layout = Layout('page', 'page')
        layout.renderer = ViewPageTemplateFile('main.pt').macros[self.macroName]
        instance = ILayoutInstance(self.context)
        instance.template = layout
        view = LayoutView(instance, self.request, name='page',
                          parent=self, page=self)
        view.body = view.layouts['body'][0]
        instance.view = view
        return view.template(view)

    @Lazy
    def resourceBase(self):
        skinSetter = self.skin and ('/++skin++' + self.skin.__name__) or ''
        # TODO: put '/@@' etc after path to site instead of directly after URL0
        return self.request.URL[0] + skinSetter + '/@@/'


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

    def getLayoutsFor(self, key):
        manager = component.getUtility(ILayoutManager)
        return manager.getLayouts('.'.join((self.name, key)), self.context)


# subview providers

class ViewLayouts(object):

    def __init__(self, view):
        self.view = view

    def __getitem__(self, key):
        view = self.view
        subviews = []
        for layout in view.getLayoutsFor(key):
            instance = ILayoutInstance(view.client)
            instance.template = layout
            v = LayoutView(instance, view.request, name=key,
                           parent=view, page=view.page)
            instance.view = v
            subviews.append(v)
        return subviews


class ViewResources(object):

    def __init__(self, view):
        self.view = view

    def __getitem__(self, key):
        # TODO...
        return []
