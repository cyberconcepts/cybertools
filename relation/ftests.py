# $Id$

import unittest, doctest
from zope.app.testing.functional import FunctionalTestCase
from zope.app.testing import setup
from zope.testbrowser.testing import Browser

from zope.app import component, intid, zapi

class BrowserTest(FunctionalTestCase):
    "Functional tests for the relation package."

    def setUp(self):
        super(BrowserTest, self).setUp()
        root = self.getRootFolder()
        sitemanager = zapi.getSiteManager(root)
        #defaultSite = component.site.LocalSiteManager(root)['default']
        default = sitemanager['default']
        intids = intid.IntIds()
        default['intids'] = intids
        reg = component.site.UtilityRegistration(u'',
                                intid.interfaces.IIntIds, default['intids'])
        key = default.registrationManager.addRegistration(reg)
        default.registrationManager[key].status = component.interfaces.registration.ActiveStatus

    def test(self):
        browser = Browser()
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        browser.addHeader('Accept-Language', 'en-US')
        browser.open('http://localhost/++etc++site/default/@@contents.html')
        self.assert_(browser.isHtml)
        addLink = browser.getLink('Relation Registry')
        addLink.click()
        self.assert_(browser.isHtml)
        inp = browser.getControl(name='new_value')
        inp.value = 'relations'
        button = browser.getControl('Apply')
        button.click()
        self.assert_(browser.isHtml)


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    #browser = FunctionalDocFileSuite('funky.txt', optionflags=flags)
    browser = unittest.makeSuite(BrowserTest)
    return unittest.TestSuite((browser,))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
