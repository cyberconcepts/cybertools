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
ZPT-based template base class.

$Id$
"""

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from cybertools.view.web import template


class Template(template.Template):

    zpt = ViewPageTemplateFile('content.pt')

    macroTemplate = ViewPageTemplateFile('main.pt')

    skin = None

    @Lazy
    def main_macro(self):
        return self.macroTemplate.macros['page']

    @Lazy
    def resourceBase(self):
        skinSetter = self.skin and ('/++skin++' + self.skin.__name__) or ''
        # TODO: put '/@@' etc after path to site instead of directly after URL0
        return self.request.URL[0] + skinSetter + '/@@/'

    def render(self, *args, **kw):
        kw['template'] = self
        return self.zpt(*args, **kw)

