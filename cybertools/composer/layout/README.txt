=================
Layout Management
=================

  ($Id$)

Let's start with some basic setup; the traversable adapter is needed for
rendering the page templates.

  >>> from zope import component
  >>> from zope.interface import Interface
  >>> from zope.traversing.adapters import DefaultTraversable
  >>> component.provideAdapter(DefaultTraversable, (Interface,))

For testing we define a simple content class.

  >>> class Document(object):
  ...     text = ''

The layout management is controlled by a global utility, the layout
manager.

  >>> from cybertools.composer.layout.base import LayoutManager, LayoutInstance
  >>> from cybertools.composer.layout.interfaces import ILayout

  >>> manager = LayoutManager()
  >>> component.provideUtility(manager)

The layouts themselves are also specified as utilities that are automatically
registered when we import the modules they are defined in.

  >>> from cybertools.composer.layout.browser import default
  >>> from cybertools.composer.layout.browser.liquid import default

In addition we have to provide at least one layout instance adapter that
connects a layout with the client object.

  >>> component.provideAdapter(LayoutInstance, (object,))


Browser Views
=============

  >>> from cybertools.composer.layout.browser.view import Page
  >>> from zope.publisher.browser import TestRequest

  >>> page = Page(Document(), TestRequest())

  >>> page()
  u'<!DOCTYPE ...>...<html ...>...</html>...'
