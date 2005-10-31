Setting up and using LazyNamespace objects
==========================================

A LazyNamespace contains variables that are only calculated when really
needed, and these are calculated only once during the lifetime of the
LazyNamespace objects they live in.

This is especially useful when rendering web pages as during this
rendering often the same data are used again and again, whereas you don't
know at the beginning of the rendering process which data you will really
need.

We first need a function that will be used to provide a value
for a variable we want to use in the LazyNamespace. This function will expect
one parameter that will be set to the LazyNamespace object when the function
is called.

Our demonstration function will increment a counter on a context object
(provided via the vars parameter) and return this counter so that we can easily
follow the calls to the function:

  >>> def getNumber(vars):
  ...     context = vars.context
  ...     context.counter += 1
  ...     return context.counter

We now register the function with our LazyNamespace class under the name
we later want to use for accessing the variable:

  >>> from cybertools.lazynamespace.lazynamespace import LazyNamespace
  >>> LazyNamespace.registerVariable('number', getNumber)

We also need a context object - that one which carries the above mentioned
counter:

  >>> from zope.interface import Interface, implements
  >>> class Number(object):
  ...    implements(Interface)
  ...    counter = 0
  >>> context = Number()

This object is now used as the context parameter when creating a LazyNamespace
object:
  
  >>> lns = LazyNamespace(context)

So let's look if the LazyNamespace object can give us a value for the variable
we have registered:

  >>> lns.number
  1

The getNumber() function has been called that apparently has
incremented the counter.

What happens if we access the variable again?

  >>> lns.number
  1

Same result, no incrementation, as it is now stored in the LazyNamespace
object and retrieved without recalculation. Really lazy...

We can even use the same function for more than one variable. When we first
access the new variable the function is called again:

  >>> LazyNamespace.registerVariable('number2', getNumber)
  >>> lns.number2
  2

Our first variable is not affected by this:

  >>> lns.number
  1

Typically you will use a LazyNamespace class for adapters. When you want
to use a LazyNamespace when rendering a browser web page you may use
a LazyBrowserNamespace:


LazyBrowserNamespace
~~~~~~~~~~~~~~~~~~~~

A LazyBrowserNamespace is meant to be used as a multi-adapter on a context
object, a request, and a view.

  >>> from cybertools.lazynamespace.lazynamespace import LazyBrowserNamespace
  >>> from cybertools.lazynamespace.interfaces import ILazyNamespace
  
  >>> import zope.component
  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer
  >>> from zope.app.publisher.interfaces.browser import IBrowserView
  >>> zope.component.provideAdapter(LazyBrowserNamespace,
  ...     (Interface, IDefaultBrowserLayer, IBrowserView),
  ...     ILazyNamespace)

We can now get at a LazyBrowserNamespace adapter using our context object
from above and supplying a request and a view in addition.

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  
  >>> class View(object):
  ...     implements(IBrowserView)
  ...     def __init__(self, context, request):
  ...         pass
  >>> view = View(context, request)
  
  >>> from zope.app import zapi
  >>> lbns = zapi.getMultiAdapter((context, request, view), ILazyNamespace)

  The LazyBrowserNamespace is independent of the LazyNamespace class and
  provides its own registry. So we won't find our variable from above
  there:
  
  >>> lbns.number
  Traceback (most recent call last):
  ...
  KeyError: 'number'

So we again register a variable, now with the LazyBrowserNamespace:
  
  >>> LazyBrowserNamespace.registerVariable('number', getNumber)
  >>> lbns.number
  3
  >>> lbns.number
  3

The old stuff from above is not affected:
  
  >>> lns.number
  1
  