==============================
Resource-oriented Architecture
==============================

  ($Id$)

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest


Providing object data in JSON format
====================================

  >>> class Demo(object):
  ...     def __init__(self, name):
  ...         self.name = name

  >>> from cybertools.roa.json import JSONView

  >>> obj = Demo('test')
  >>> jsv = JSONView(obj, TestRequest())
