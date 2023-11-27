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

import os
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope import component


generic_page = ViewPageTemplateFile('generic.pt')
view_macros = ViewPageTemplateFile(os.path.join('liquid', 'view_macros.pt'))


class BaseView(object):

    index = generic_page
    default_template = template = view_macros     # specify in subclass
    resource_prefix = '/@@/'
    view_mode = 'view'

    def wrap(self):
        return self

    def __call__(self):
        return self.index(self)

    def update(self):
        return True

    def mainMacro(self):
        return view_macros.macros['main']

    #@rcache
    def defaultMacros(self):
        return self.default_template.macros

    def macros(self):
        return self.template.macros

    def contentMacro(self):
        return self.macros()[getattr(self, 'content_renderer', 'content')]

    #@rcache
    def homeURL(self):
        return '/'

    @Lazy
    def resources(self):
        return {'base.css': '%sbase.css' % self.resource_prefix}

    @Lazy
    def actions(self):
        return dict(top=[], portlet_left=[], portlet_right=[])


# generic views for use with generic persistent objects with type-based adapters
# (not used at the moment - obsolete?)

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
