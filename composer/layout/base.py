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

from zope.cachedescriptors.property import Lazy
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

    @Lazy
    def regions(self):
        result = {}
        for name, layout in component.getUtilitiesFor(ILayout):
            region = result.setdefault(layout.regionName,
                                       Region(layout.regionName))
            region.layouts.append(layout)
        return result

    def getLayouts(self, key, instance):
        region = self.regions.get(key)
        return sorted(instance.getLayouts(region),
                      key=lambda x: x.template.order)


class Layout(Template):

    implements(ILayout)

    title = description = u''
    category = 'default'
    renderer = None
    instanceName = ''
    order = 50
    sublayouts = None

    def __init__(self, name, regionName, **kw):
        self.name = name
        self.regionName = regionName
        for k, v in kw.items():
            setattr(self, k, v)
        self.register()

    def register(self):
        existing = component.queryUtility(ILayout, name=self.name)
        if existing:
            raise ValueError("Layout '%s' has already been registered." % self.name)
        component.provideUtility(self, provides=ILayout, name=self.name)


class LayoutInstance(object):

    implements(ILayoutInstance)

    template = None

    def __init__(self, context):
        self.context = context

    @property
    def renderer(self):
        return self.template.renderer

    def getLayouts(self, region):
        """ Return sublayout instances.
        """
        if region is None:
            return []
        result = []
        sublayouts = self.template.sublayouts
        for l in region.layouts:
            if sublayouts is None or l.name in sublayouts:
                li = component.getAdapter(self.context, ILayoutInstance,
                                          name=l.instanceName)
                li.template = l
                result.append(li)
        return result
