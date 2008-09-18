=================
Layout Management
=================

  ($Id$)

  >>> from zope import component
  >>> from zope.interface import Interface

  >>> from cybertools.composer.layout.base import LayoutManager
  >>> manager = LayoutManager()
  >>> component.provideUtility(manager)

  >>> from zope.traversing.adapters import DefaultTraversable
  >>> component.provideAdapter(DefaultTraversable, (Interface,))


Browser Views
=============

  >>> from zope.app.pagetemplate import ViewPageTemplateFile
  >>> standardRenderers = ViewPageTemplateFile('browser/standard.pt').macros

  >>> from cybertools.composer.layout.base import Layout
  >>> from cybertools.composer.layout.interfaces import ILayout

  >>> #css = Layout('page.css', renderer=standardRenderers['css'])
  >>> # css = ResourceCollection('css', resourceRenderers['css'])
  >>> #component.provideUtility(css, ILayout, name='css')

  >>> from cybertools.composer.layout.browser.liquid.default import BodyLayout
  >>> bodyLayout = BodyLayout()
  >>> component.provideUtility(bodyLayout, ILayout, name='body.liquid')

  >>> footerLayout = Layout('body.footer', renderer=standardRenderers['footer'])
  >>> component.provideUtility(footerLayout, ILayout, name='footer.default')

  >>> from cybertools.composer.layout.browser.view import Page
  >>> from zope.publisher.browser import TestRequest
  >>> page = Page(None, TestRequest())

  >>> page()
  u'<!DOCTYPE ...>...<html ...>...</html>...'
