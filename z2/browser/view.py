#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
Base classes for views.

$Id$
"""

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope import component
from Products.Five import BrowserView
#from Products.Five.browser.pagetemplatefile import PageTemplateFile


generic_page = ViewPageTemplateFile('generic.pt')
view_macros = ViewPageTemplateFile('view_macros.pt')


class BaseView(BrowserView):

    index = generic_page
    default_template = None     # specify in subclass

    def __call__(self):
        return self.index(self)

    def getMainMacro(self):
        return view_macros.macros['main']

    def getDefaultTemplate(self):
        return self.default_template

    def getContentMacro(self):
        return self.getDefaultTemplate().macros[self.content_renderer]


# generic views for use with generic persistent objects with type-based adapters

class GenericView(BaseView):

    name = 'index_html'

    @Lazy
    def object(self):
        return self.context.typeInterface(self.context)

    @Lazy
    def objectView(self):
        return component.getMultiAdapter((self.object, self.request), name=self.name)

    def __call__(self):
        return self.objectView()


class GenericAddForm(GenericView):

    name = 'create.html'
