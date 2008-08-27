=================
Layout Management
=================

  ($Id$)

  >>> from zope import component
  >>> from zope.interface import Interface

  >>> from cybertools.composer.layout.base import LayoutManager
  >>> component.provideUtility(LayoutManager())

  >>> from cybertools.composer.layout.base import Layout, LayoutInstance
  >>> from cybertools.composer.layout.browser.liquid.default import BodyLayout


Browser Views
=============

  >>> from zope.app.pagetemplate import ViewPageTemplateFile
  >>> standardRenderers = ViewPageTemplateFile('browser/standard.pt').macros

  >>> from zope.traversing.adapters import DefaultTraversable
  >>> component.provideAdapter(DefaultTraversable, (Interface,))

  >>> css = Layout()  # ResourceCollection()
  >>> css.renderer = standardRenderers['css'] # resourceRenderers['css']
  >>> css.registerFor('page.css')

  >>> bodyLayout = BodyLayout()
  >>> bodyLayout.registerFor('page.body')

  >>> footerLayout = Layout()
  >>> footerLayout.renderer = standardRenderers['footer']
  >>> footerLayout.registerFor('body.footer')

  >>> from cybertools.composer.layout.browser.view import Page
  >>> from zope.publisher.browser import TestRequest
  >>> page = Page(None, TestRequest())

  >>> page()
  u'<!DOCTYPE ...>...<html ...>...</html>...'
