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
Generic view base class.

$Id$
"""

from cybertools.web.template import Template


class View(object):

    templateFactory = Template

    _template = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def template(self):
        if self._template is None and self.templateFactory:
            self._template = self.templateFactory(self)
        return self._template

    def render(self, *args, **kw):
        return self.template.render(*args, **kw)

