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
Basic classes for layouts and layout components.

$Id$
"""

from zope import component
from zope.interface import implements

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.layout.interfaces import ILayoutManager
from cybertools.composer.layout.interfaces import ILayout, ILayoutInstance
from cybertools.composer.layout.region import Region
from cybertools.util.jeep import Jeep


class LayoutManager(object):

    implements(ILayoutManager)

    def __init__(self):
        self.regions = {}

    def register(self, layout, regionName):
        region = self.regions.setdefault(regionName, Region(regionName))
        region.layouts.append(layout)


class Layout(Template):

    implements(ILayout)

    name = u''
    manager = None
    renderer = None


class LayoutInstance(object):

    implements(ILayoutInstance)

    def __init__(self, template, context=None):
        self.template = template
        self.context = context

    def registerFor(self, regionName):
        manager = component.getUtility(ILayoutManager)
        manager.register(self, regionName)

    @property
    def renderer(self):
        return self.template.renderer
