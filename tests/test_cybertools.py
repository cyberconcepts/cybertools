# $Id$

import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import ztapi
from zope.interface.verify import verifyClass
#from zope.app.tests.setup import placelessSetUp
from zope.app.testing.setup import placefulSetUp
from zope.app.container.interfaces import IContained
from zope.app.folder import Folder
from zope.app import zapi

from cybertools.menu import Menu
from cybertools.interfaces import IMenu

class TestMenu(unittest.TestCase):
    "Test methods of the Menu class."

    def setUp(self):
#        placelessSetUp()
        placefulSetUp()
        self.f1 = Folder()
        self.f1.__name__ = u'f1'
        self.m1 = Menu()
        self.f1['m1'] = self.m1

    def tearDown(self):
        pass

    # the tests...

    def testInterface(self):
        self.assert_(IMenu.providedBy(Menu()),
            'Interface IMenu is not implemented by class Menu.')
        self.assert_(IContained.providedBy(Menu()),
            'Interface IContained is not implemented by class Menu.')
        verifyClass(IMenu, Menu)

def test_suite():
    return unittest.TestSuite((
            unittest.makeSuite(TestMenu),
            DocFileSuite('../doc/menu.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
