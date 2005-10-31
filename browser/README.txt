Use Content Providers and Viewlets for setting up web pages
===========================================================

We first set up a test and working environment:

    >>> from zope.app import zapi
    >>> from zope.app.testing import ztapi
    >>> from cybertools.browser.pageprovider import BaseView, PageProviderView
    >>> from cybertools.browser.pageprovider import PageProvider

    