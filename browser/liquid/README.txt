The Liquid Skin and Related Stuff
=================================

We first set up a test and working environment:

    >>> from zope.app import zapi
    >>> from zope.app.testing import ztapi
    >>> from zope.app.component import site, interfaces

    >>> from zope.testbrowser import Browser
    >>> browser = Browser()
    >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

We can now open a page using the Liquid skin:
    
    >>> browser.addHeader('Accept-Language', 'en-US')
    >>> browser.open('http://localhost/++skin++Liquid')
    >>> print browser.headers
    Status: 200 Ok...
    
    >>> browser.url
    'http://localhost/++skin++Liquid'
    