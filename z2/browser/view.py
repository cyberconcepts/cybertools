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

from Acquisition import aq_chain
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cybertools.view.browser.view import BaseView, GenericView


main_page = ViewPageTemplateFile('main.pt')
zmi_page = ViewPageTemplateFile('main_zmi.pt')


class BaseView(BrowserView, BaseView):

    # make Zope 2 restricted Python happy
    __allow_access_to_unprotected_subobjects__ = 1
    def wrap(self):
        if len(aq_chain(self)) < 2:
            return self.__of__(self.context)
        return self

    resource_prefix = '/++resource++'
    template_name = 'view_macros'
    content_renderer = 'content'

    def defaultMacros(self):
        template = getattr(self.context, self.template_name, None)
        if template is None:
            return super(BaseView, self).defaultMacros()
        return template.macros

    def contentMacro(self):
        macroName = self.content_renderer
        macro = self.defaultMacros().get(macroName)
        if macro is None:
            return super(BaseView, self).defaultMacros()[macroName]
        return macro


# generic views for use with generic persistent objects with type-based adapters
# (not used at the moment - obsolete?)

class GenericView(BaseView, GenericView):

    def __call__(self):
        return GenericView.__call__(self)


class GenericAddForm(GenericView):

    name = 'create.html'
