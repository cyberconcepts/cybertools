===============================
All about Views, Templates, ...
===============================

$Id$


Basic (Generic) Browser Views
=============================


Generic Views (Obsolete)
========================

(This was an attempt to develop a really generic view framework base on
the `PAC <http://en.wikipedia.org/wiki/Presentation-abstraction-control>`_
patten, that was never used in a real application.
The cybertools.view.web package is kept because it is directly
referenced by package-includes entries in live installations.)

OK, there aren't really generic views. Already the first implementation we
want to look at is a specic one: It is based on Zope Page Templates and
uses the classic CMF/Zope 3 approach: The template belonging to a view - more
precisely a page - calls a `main` macro and fills a slot there. But at least
the template implementation is decoupled from the view, so we are able to
put a lot of generic functionality into the view.

In order to make a ZPT work we need a Zope-compatible request, so we use
the standard Zope 3 TestRequest.

  >>> from zope.publisher.browser import TestRequest

  >>> from cybertools.view.web.base import Page, Content
  >>> request = TestRequest()
  >>> view = Page(None, request)
  >>> view.render()
  u'...<html...>...<body...>...</body>...</html>...'

