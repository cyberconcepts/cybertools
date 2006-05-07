Browser View Tools
==================

We first set up a test and working environment:

  >>> from zope.app import zapi
  >>> from zope.app.testing import ztapi
    
  >>> from zope import component, interface
  >>> from zope.publisher.browser import TestRequest
  >>> from zope.publisher.interfaces.browser import IBrowserRequest

The View Controller
-------------------

There is a special view class that does not directly adapt to a real context
(i.e. typically a content) object but to a view instead. Thus it can provide
additional functionality e.g. for templates without the view being aware
of it.

This view controller (or controller view) is typically provided by the
Controller class. Let's use the Controller sub-class from the Liquid skin
because this already provides some predefined stuff:

  >>> from cybertools.browser.liquid.controller import Controller

Before creating a controller we have to set up a context object and
a view:
  
  >>> class SomeObject(object): pass
  >>> obj = SomeObject()
  >>> class View(object):
  ...     def __init__(self, context, request):
  ...         self.context = context
  ...         self.request = request
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = View(obj, request)
  
  >>> controller = Controller(view, request)
  >>> controller.view is view
  True
  >>> controller.context is obj
  True
  >>> controller.request is request
  True

The controller registers itself with the view:

  >>> view.controller is controller
  True

The resourceBase attribute gives a base URL to which one can simply append
the name of a resource.

  >>> controller.resourceBase
  'http://127.0.0.1/@@/'

If necessary, a ++skin++xxx path element is provided
with the resourceBase to care for proper skin setting. This will work only
(and is only necessary) when the skin is set programmatically

  >>> class DummySkin(object): pass
  >>> skin = DummySkin; skin.__name__ = 'dummy'

Note that we make heavy use of Lazy attributes, so we have to get a new
controller object to get an updated setting:

  >>> controller = Controller(view, request)
  >>> controller.skin = skin
  >>> controller.resourceBase
  'http://127.0.0.1/++skin++dummy/@@/'

The controller may be used as a provider for content elements using
ZPT macros:

  >>> cssMacros = controller.macros['css']
  >>> len(cssMacros)
  4
  >>> m1 = cssMacros[0]
  >>> print m1.name, m1.media, m1.resourceName
  css all zope3_tablelayout.css

Calling a macro provided by Controller.macros[] returns the real ZPT macro:

  >>> m1()
  [...base_macros.pt...css...]

The pre-set collection of macros for a certain slot may be extended:

  >>> controller.macros.register('css', resourceName='node.css', media='all')
  >>> len(controller.macros['css'])
  5
  >>> m5 = cssMacros[4]
  >>> print m5.name, m5.media, m5.resourceName
  css all node.css


The View Configurator
---------------------

A view configurator is a multiadapter for a content object that provides
a set of properties to be used for setting up special presentation
characteristics of a page. Typical examples for such characteristics are

- the skin to be used
- the logo to show in the corner of the page

The default configurator uses attribute annotations for retrieving view
properties; that means that there could be form somewhere to edit those
properties and store them in the content object's annotations.

The configurator is called automatically from the controller if there is
an appropriate adapter:

  >>> from cybertools.browser.configurator import IViewConfigurator
  >>> from cybertools.browser.configurator import ViewConfigurator
  >>> component.provideAdapter(ViewConfigurator, (SomeObject, IBrowserRequest),
  ...                          IViewConfigurator)
  >>> controller = Controller(view, request)

But this does not have any effect as long as there aren't any properties
stored in the attribute annotations. So let's set a 'skinName' attribute:

  >>> from zope.app.annotation.interfaces import IAttributeAnnotatable, IAnnotations
  >>> from zope.app.annotation.attribute import AttributeAnnotations
  >>> interface.classImplements(SomeObject, IAttributeAnnotatable)
  >>> component.provideAdapter(AttributeAnnotations, (SomeObject,), IAnnotations)
  >>> ann = IAnnotations(obj)
  >>> setting = {'skinName': {'value': 'SuperSkin'}}
  >>> from cybertools.browser.configurator import ANNOTATION_KEY
  >>> ann[ANNOTATION_KEY] = setting

  >>> controller = Controller(view, request)
  >>> controller.skinName.value
  'SuperSkin'

