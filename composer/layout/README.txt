=================
Layout Management
=================

  ($Id$)

  >>> from zope import component
  >>> from zope.interface import Interface

  >>> from cybertools.composer.layout.base import LayoutManager
  >>> component.provideUtility(LayoutManager())

  >>> from cybertools.composer.layout.base import Layout, LayoutInstance


Browser Views
=============

  >>> from zope.traversing.adapters import DefaultTraversable
  >>> component.provideAdapter(DefaultTraversable, (Interface,))

  >>> from cybertools.composer.layout.browser.layout import PageLayout
  >>> pageLayout = PageLayout()
  >>> pageLayoutInstance = LayoutInstance(pageLayout)

  >>> from zope.app.pagetemplate import ViewPageTemplateFile

  >>> bodyLayout = Layout()
  >>> bodyLayout.renderer = ViewPageTemplateFile('browser/liquid/body.pt').macros['body']
  >>> LayoutInstance(bodyLayout).registerFor('page.body')

  >>> standardRenderers = ViewPageTemplateFile('browser/standard.pt').macros
  >>> footerLayout = Layout()
  >>> footerLayout.renderer = standardRenderers['footer']
  >>> LayoutInstance(footerLayout).registerFor('body.footer')

  >>> from cybertools.composer.layout.browser.view import Page
  >>> from zope.publisher.browser import TestRequest
  >>> page = Page(pageLayoutInstance, TestRequest())

  >>> page()
  u'<!DOCTYPE ...>...<html ...>...</html>...
