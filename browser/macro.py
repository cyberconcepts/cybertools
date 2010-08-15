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
Wrapping ZPT macro templates for dynamic macro lookup.

$Id$
"""

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy


_not_found = object()


class MacroTemplate(object):

    def __init__(self, template, parent=None):
        self.baseTemplate = template
        self.parent = parent

    @Lazy
    def macros(self):
        return Macros(self)


class Macros(dict):

    def __init__(self, template):
        self.template = template

    def __getitem__(self, key):
        macro = self.template.baseTemplate.macros.get(key, _not_found)
        if macro is _not_found:
            parent = self.template.parent
            if parent is None:
                raise KeyError(key)
            return parent.macros[key]
        return macro
