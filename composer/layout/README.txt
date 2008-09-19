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

The layouts themselves are also specified as utilities.

  >>> #from cybertools.composer.layout.browser.liquid.default import css
  >>> #component.provideUtility(css, ILayout, name='css')

  >>> from cybertools.composer.layout.browser.liquid.default import body
  >>> component.provideUtility(body, ILayout, name='body.liquid')

  >>> from cybertools.composer.layout.browser.default import footer
  >>> component.provideUtility(footer, ILayout, name='footer.default')

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
