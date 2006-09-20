Browser View Tools
==================

  >>> from zope import component, interface
  >>> from zope.interface import Interface, implements
  >>> from zope.publisher.interfaces.browser import IBrowserRequest

The Generic View class
----------------------

GenericView is intended as the base class for application-specific views.
The GenericView class itself provides only basic functionality, so you
will have to subclass it. (An example can be found in loops.browser - see
the common and node modules there.)

Let's start with a dummy content object and create a view on it:

  >>> class SomeObject(object):
  ...     implements(Interface)
  >>> obj = SomeObject()

  >>> from cybertools.browser.view import GenericView
  >>> class View(GenericView): pass

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = View(obj, request)

Via the `template` and `macro` attributes one may control the presentation of
the view - in fact the rendering of a certain content object is achieved
by providing an appropriate macro for its view.

The view also may provide a special skin and a menu.

All these attributes default to None:

  >>> view.template is None
  True
  >>> view.macro is None
  True
  >>> view.skin is None
  True
  >>> view.menu is None
  True

The `item` attribute may be used to delegate to another view; it defaults to
self:

  >>> view.item is view
  True

There is a method for setting the skin that will be called when the controller
attribute is set, see below:

  >>> view.setSkin(None)

When the view is called, the standard main template (main.pt) is rendered;
this template in turn calls the view's pageBody() method to render the
body.

This pageBody() method returns the rendered body by accessing another view
(default: BodyTemplateView) that provides a corresponding template in its
bodyTemplate attribute.


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

  >>> controller = Controller(view, request)
  >>> controller.view is view
  True
  >>> controller.context is obj
  True
  >>> controller.request is request
  True
  >>> request.annotations['cybertools.browser']['controller'] == controller
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

The controller may be used as a provider for HTML elements using
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

The pre-set collection of macros for a certain slot may be extended
(this may be done by overriding the view's setupController() method, e.g.):

  >>> controller.macros.register('css', 'node.css', resourceName='node.css', media='all')
  >>> len(controller.macros['css'])
  5
  >>> m5 = cssMacros[4]
  >>> print m5.name, m5.media, m5.resourceName
  css all node.css

If an identifier is given (the second parameter) a certain macro is only
registered once; note: the first setting will not be overridden!

  >>> controller.macros.register('css', 'node.css', resourceName='node.css')
  >>> len(controller.macros['css'])
  5

We can also access slots that are not predefined:

  >>> controller.macros['js.execute']
  []

  >>> jsCall = 'dojo.require("dojo.widget.Editor")'
  >>> controller.macros.register('js-execute', jsCall, jsCall=jsCall)
  >>> dojoCall = controller.macros['js-execute'][0]
  >>> dojoCall()
  [...base_macros.pt...macro/jsCall...]


The View Configurator
---------------------

A view configurator is typically a multiadapter for a content object that provides
a set of properties to be used for setting up special presentation
characteristics of a page. Typical examples for such characteristics are

- the skin to be used
- the logo to show in the corner of the page

The default configurator uses attribute annotations for retrieving view
properties; that means that there could be a form somewhere to edit those
properties and store them in the content object's annotations.

  >>> from zope.app.annotation.interfaces import IAttributeAnnotatable, IAnnotations
  >>> from zope.app.annotation.attribute import AttributeAnnotations
  >>> component.provideAdapter(AttributeAnnotations, (SomeObject,), IAnnotations)

The configurator is called automatically from the controller if there is
an appropriate adapter:

  >>> from cybertools.browser.configurator import IViewConfigurator
  >>> from cybertools.browser.configurator import ViewConfigurator
  >>> component.provideAdapter(ViewConfigurator, (SomeObject, IBrowserRequest),
  ...                          IViewConfigurator)
  >>> controller = Controller(view, request)

But this does not have any effect as long as there aren't any properties
stored in the attribute annotations. So let's set a 'skinName' attribute:

  >>> interface.classImplements(SomeObject, IAttributeAnnotatable)
  >>> ann = IAnnotations(obj)
  >>> setting = {'skinName': {'value': 'SuperSkin'}}
  >>> from cybertools.browser.configurator import ANNOTATION_KEY
  >>> ann[ANNOTATION_KEY] = setting

  >>> controller = Controller(view, request)
  >>> controller.skinName.value
  'SuperSkin'

Another way of providing view configurations is using a view configurator
as a utility, this can be used for setting view properties by certain
packages.

  >>> from cybertools.browser.configurator import GlobalViewConfigurator
  >>> component.provideUtility(GlobalViewConfigurator())

  >>> gvc = component.getUtility(IViewConfigurator)


Processing form input
---------------------

GenericView also provides an update() method that may be called from
templates that might receive form information.

  >>> view.update()
  True

Real work can only be done by an adapter to GenericView that provides the
IFormController interface with its update(). There also must be a
form variable (typically coming from a hidden field) with the name
'form.action' that provides the name under which the form controller is
registered.

  >>> from cybertools.browser.controller import IFormController, FormController
  >>> class MyController(FormController):
  ...     def update(self):
  ...         print 'updating...'

  >>> component.provideAdapter(MyController, (View, IBrowserRequest),
  ...                          IFormController, name='save')

  >>> request = TestRequest(form={'form.action': 'save'})
  >>> view = View(obj, request)
  >>> view.update()
  updating...
  True

The update() method will only be executed once:

  >>> view.update()
  True


