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

  >>> from cybertools.composer.layout.browser.default import page
  >>> component.provideUtility(page, ILayout, name='page')

  >>> from cybertools.composer.layout.browser.liquid.default import css
  >>> component.provideUtility(css, ILayout, name='css.liquid')

  >>> from cybertools.composer.layout.browser.liquid.default import body
  >>> component.provideUtility(body, ILayout, name='body.liquid')

  >>> from cybertools.composer.layout.browser.default import logo
  >>> component.provideUtility(logo, ILayout, name='logo.default')

  >>> from cybertools.composer.layout.browser.default import top_actions
  >>> component.provideUtility(top_actions, ILayout, name='top_actions.default')

  >>> from cybertools.composer.layout.browser.default import column1
  >>> component.provideUtility(column1, ILayout, name='column1.default')

  >>> from cybertools.composer.layout.browser.default import content
  >>> component.provideUtility(content, ILayout, name='content.default')

  >>> from cybertools.composer.layout.browser.default import column2
  >>> component.provideUtility(column2, ILayout, name='column2.default')

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
