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
A view configurator provides configuration data for a view controller.

$Id$
"""

from zope.app import zapi
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope.cachedescriptors.property import Lazy
from zope.interface import Interface, Attribute, implements
from zope.component import adapts


# interfaces

class IViewConfigurator(Interface):
    """ Usually implemented by an adapter (e.g. to IAnnotatable);
        provides a set of properties that govern the appearance of a
        page, e.g. the name of the logo, CSS file(s), or portlets.
    """

    viewProperties = Attribute('A sequence of IViewProperty objects')

    def getActiveViewProperties(self):
        """ Return a selection of this configurator's view properties
            that are to be considered active in the current context.
        """


class IViewProperty(Interface):

    slot = Attribute('The property slot to fill')
    name = Attribute('The name of the object to fill the slot')


class IMacroViewProperty(IViewProperty):

    slot = Attribute('The property slot to fill')
    name = Attribute('The name of the macro to use; may be None, '
                      'meaning that the slot name will be used')
    template = Attribute('The template providing the macro')
    params = Attribute('A mapping with parameters (key/value pairs) '
                       'to be handed over to the macro')


#default implementations

ANNOTATION_KEY = 'cybertools.browser.configurator.ViewConfigurator'

class ViewConfigurator(object):
    """ Simple/basic default adapter using attribute annotations as storage
        for view properties.
    """

    implements(IViewConfigurator)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def viewProperties(self):
        ann = IAnnotations(self.context)
        propDefs = ann.get(ANNOTATION_KEY, {})
        return [self.setupViewProperty(prop, propDef)
                    for prop, propDef in propDefs.items() if propDef]
        # idea: include properties from GlobalViewConfigurator;
        # there also may be other view configurators e.g. based on
        # the class (or some sort of type) of the context object.
        # Also the view properties may be filtered by permission
        # or other conditions.
        # Note: collecting configurators may be solved by getting
        # multiple configurators (+ utilities) in the controller!

    def getActiveViewProperties(self):
        return self.viewProperties

    def setupViewProperty(self, prop, propDef):
        vp = zapi.queryMultiAdapter((self.context, self.request),
                                    IViewProperty, name=prop)
        if vp is None:
            vp = ViewProperty(self.context, self.request)
        vp.slot = prop
        vp.setParams(propDef)
        return vp


class GlobalViewConfigurator(object):
    """ A global utility that allows the registration of view properties.
    """

    implements(IViewConfigurator)

    def __init__(self):
        self.viewProperties = []

    def getActiveViewProperties(self):
        return self.viewProperties


class ViewProperty(object):

    implements(IViewProperty)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.slot = None
        self.name = None
        self.value = None
        self.params = {}

    def setParams(self, params):
        params = dict(params)
        self.name = params.pop('name', '')
        self.value = params.pop('value', None)
        self.params = params


class MacroViewProperty(object):

    implements(IMacroViewProperty)

    template = None

    def setParams(self, params):
        params = dict(params)
        self.name = params.pop('name', '')
        self.identifier = params.pop('identifier', name)
        self.template = params.pop('template', None)
        self.params = params
