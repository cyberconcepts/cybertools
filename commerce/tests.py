#! /usr/bin/python

"""
Tests for the 'cybertools.commerce' package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite

from zope.app.intid.interfaces import IIntIds
from zope import component
from zope.interface import implements

from cybertools.commerce.order import OrderItems
from cybertools.commerce.product import Product


class IntIdsStub(object):
    """A testing stub (mock utility) for IntIds."""
    implements(IIntIds)

    def __init__(self):
        self.objs = []

    def getObject(self, uid):
        return self.objs[uid]

    def register(self, ob):
        if ob not in self.objs:
            self.objs.append(ob)
        return self.objs.index(ob)

    getId = register
    queryId = getId

    def unregister(self, ob):
        id = self.getId(ob)
        self.objs[id] = None

    def __iter__(self):
        return iter(xrange(len(self.objs)))


def setUp(testCase):
    component.provideUtility(IntIdsStub())
    component.provideAdapter(OrderItems)

def tearDown(testCase):
    pass


class Test(unittest.TestCase):
    "Basic tests."

    def testBasicStuff(self):
        p = Product('p001')


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        DocFileSuite('README.txt', optionflags=flags,
                     setUp=setUp, tearDown=tearDown),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
