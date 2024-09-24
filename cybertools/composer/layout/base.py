# cybertools.composer.layout.base

""" Basic classes for layouts and layout components.
"""

from zope.cachedescriptors.property import Lazy
from zope import component
from zope.interface import implementer

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.layout.interfaces import ILayoutManager
from cybertools.composer.layout.interfaces import ILayout, ILayoutInstance
from cybertools.composer.layout.region import Region
from cybertools.util.jeep import Jeep


@implementer(ILayoutManager)
class LayoutManager(object):

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


@implementer(ILayout)
class Layout(Template):

    title = description = u''
    category = 'default'
    renderer = None
    instanceName = ''
    order = 50
    sublayouts = None
    defaultSublayout = None

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


@implementer(ILayoutInstance)
class LayoutInstance(object):

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
