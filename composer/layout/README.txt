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

  >>> from zope.app.pagetemplate import ViewPageTemplateFile

  >>> #pageLayout = Layout()
  >>> #pageLayout.renderer = ViewPageTemplateFile('browser/main.pt').macros['page']

  >>> bodyLayout = Layout()
  >>> bodyLayout.renderer = ViewPageTemplateFile('browser/liquid/body.pt').macros['body']
  >>> bodyLayout.registerFor('page.body')

  >>> footerLayout = Layout()
  >>> standardRenderers = ViewPageTemplateFile('browser/standard.pt').macros
  >>> footerLayout.renderer = standardRenderers['footer']
  >>> footerLayout.registerFor('body.footer')

  >>> from cybertools.composer.layout.browser.view import Page
  >>> from zope.publisher.browser import TestRequest
  >>> #instance = LayoutInstance(None)
  >>> #instance.template = pageLayout
  >>> #page = Page(instance, TestRequest())
  >>> page = Page(None, TestRequest())

  >>> page()
  u'<!DOCTYPE ...>...<html ...>...</html>...
