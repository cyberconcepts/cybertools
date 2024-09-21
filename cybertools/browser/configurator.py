# cybertools.browser.configurator

""" A view configurator provides configuration data for a view controller.
"""

from zope import component
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope.cachedescriptors.property import Lazy
from zope.interface import Interface, Attribute, implementer


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

@implementer(IViewConfigurator)
class ViewConfigurator(object):
    """ An base class for adapters that allow the registration of view properties.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.viewProperties = []

    def getActiveViewProperties(self):
        return self.viewProperties


ANNOTATION_KEY = 'cybertools.browser.configurator.ViewConfigurator'

class AnnotationViewConfigurator(ViewConfigurator):
    """ Simple adapter using attribute annotations as storage
        for view properties.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def viewProperties(self):
        ann = IAnnotations(self.context)
        propDefs = ann.get(ANNOTATION_KEY, {})
        return [self.setupViewProperty(prop, propDef)
                    for prop, propDef in propDefs.items() if propDef]

    def getActiveViewProperties(self):
        return self.viewProperties

    def setupViewProperty(self, prop, propDef):
        vp = component.queryMultiAdapter((self.context, self.request),
                                    IViewProperty, name=prop)
        if vp is None:
            vp = ViewProperty(self.context, self.request)
        vp.slot = prop
        vp.setParams(propDef)
        return vp


@implementer(IViewProperty)
class ViewProperty(object):

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


@implementer(IMacroViewProperty)
class MacroViewProperty(ViewProperty):

    template = None

    def setParams(self, params):
        params = dict(params)
        self.slot = params.pop('slot', '')
        self.name = params.pop('name', None)
        self.identifier = params.pop('identifier', self.name)
        self.template = params.pop('template', None)
        self.params = params
