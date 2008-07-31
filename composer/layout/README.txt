=================
Layout Management
=================

  ($Id$)

  >>> from zope import component
  >>> from zope.interface import Interface

  >>> from cybertools.composer.layout.base import Layout, LayoutInstance
  >>> from cybertools.composer.layout.region import Region, regions


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
  >>> bodyRegion = Region('body')
  >>> bodyRegion.layouts.append(LayoutInstance(bodyLayout))
  >>> regions['page.body'] = bodyRegion

  >>> standardRenderers = ViewPageTemplateFile('browser/standard.pt').macros
  >>> footerLayout = Layout()
  >>> footerLayout.renderer = standardRenderers['footer']
  >>> footerRegion = Region('footer')
  >>> footerRegion.layouts.append(LayoutInstance(footerLayout))
  >>> regions['body.footer'] = footerRegion

  >>> from cybertools.composer.layout.browser.view import Page
  >>> from zope.publisher.browser import TestRequest
  >>> page = Page(pageLayoutInstance, TestRequest())

  >>> page()
  u'<!DOCTYPE ...>...<html ...>...</html>...
