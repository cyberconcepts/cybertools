=================================================================
Supporting the Zope2 Environment for Zope3/ZTK-based Applications
=================================================================

  ($Id$)

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest


Views
=====

  >>> from zope.traversing.adapters import DefaultTraversable
  >>> component.provideAdapter(DefaultTraversable, (object,))

  >>> from cybertools.z2.browser.view import BaseView
  >>> view = BaseView(object(), TestRequest())

  >>> html = view()
