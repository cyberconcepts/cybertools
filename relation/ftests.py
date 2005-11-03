# $Id$

import unittest, doctest
from zope.app.testing.functional import FunctionalTestCase
from zope.testbrowser import Browser

class BrowserTest(FunctionalTestCase):
    "Functional tests for the relation package."

    def test(self):
        browser = Browser()
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        browser.addHeader('Accept-Language', 'en-US')
        browser.open('http://localhost/++etc++site/default/@@contents.html')
        self.assert_(browser.isHtml)
        addLink = browser.getLink('Relations Registry Utility')
        addLink.click()
        self.assert_(browser.isHtml)
        inp = browser.getControl(name='new_value')
        inp.value = 'relations'
        button = browser.getControl('Apply')
        button.click()
        self.assert_(browser.isHtml)
        

def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    #browser = FunctionalDocFileSuite('skin/cyberview.txt', optionflags=flags)
    browser = unittest.makeSuite(BrowserTest)
    return unittest.TestSuite((browser,))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
