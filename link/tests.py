# $Id$

import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.interface.verify import verifyClass
from zope.interface import implements
from zope.app.intid.interfaces import IIntIds


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


class TestLink(unittest.TestCase):
    "Basic tests for the link package."

    def testBasics(self):
        pass


def test_suite():
    return unittest.TestSuite((
                unittest.makeSuite(TestLink),
                DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
