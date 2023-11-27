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
Use ZPT macros as layout renderers.

$Id$
"""

from zope.app.pagetemplate import ViewPageTemplateFile

from cybertools.util.cache import cache


class RendererFactory(object):
    """ Provider for ZPT macros.
    """

    def __init__(self, template):
        self.template = template

    def get(self, key, default=None):
        return self.template.macros.get(key, default)

    def __getitem__(self, key):
        #return self.template.macros[key]
        return Renderer(key, self)

    def __getattr__(self, key):
        """ Convenience method.
        """
        #return lambda key=key: self[key]
        return self[key]

    def __repr__(self):
        return ('<RendererFactory, template=%r, macros=%r>' %
                    (self.template, self.template.macros.keys()))


class Renderer(object):

    def __init__(self, name, factory):
        self.name = name
        self.factory = factory
        self.template = factory.template

    def __call__(self):
        return self.template.macros[self.name]


rendererTemplate = ViewPageTemplateFile('renderer.pt')

class CachableRenderer(object):

    lifetime = 3 * 3600
    #lifetime = 24 * 3600

    def __init__(self, view, renderer):
        self.view = view
        self.renderer = renderer

    def getRenderMacroId(self, *args):
        return 'renderer.' + '.'.join(args)

    @cache(getRenderMacroId, lifetime=lifetime)
    def renderMacro(self, *args):
        return rendererTemplate(self.view, view=self.view, macro=self.renderer)


