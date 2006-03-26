#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
Controller for views, templates, macros.

$Id$
"""

from zope.app import zapi
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy


class Controller(object):

    def __init__(self, context, request):
        self.view = context         # the controller is adapted to a view
        self.context = context.context
        self.request = request
        self.skin = None            # may be overwritten by the view
        context.controller = self   # notify the view

    @Lazy
    def macros(self):
        return Macros(self)

    @Lazy
    def resourceBase(self):
        skinSetter = self.skin and ('/++skin++' + self.skin.__name__) or ''
        # TODO: put '/@@' etc after path to site instead of directly after URL0
        return self.request.URL[0] + skinSetter + '/@@/'


class Macros(dict):

    # TODO: move to namedTemplate
    standardTemplate = ViewPageTemplateFile('base_macros.pt')

    def __init__(self, controller):
        self.controller = controller

    def register(self, slot, template=None, name=None, position=None, **kw):
        if template is None:
            template = self.standardTemplate
        if name is None:
            name = slot
        macro = Macro(template, name, **kw)
        if slot not in self:
            self[slot] = []
        if position is None:
            self[slot].append(macro)
        else:
            self[slot].insert(position, macro)

class Macro(object):

    def __init__(self, template, name, **kw):
        self.template = template
        self.name = name
        for k in kw:
            setattr(self, k, kw[k])

    @Lazy
    def macro(self):
        return self.template.macros[self.name]

    def __call__(self):
        return self.macro

