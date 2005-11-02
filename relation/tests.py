# $Id$

import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import ztapi
from zope.interface.verify import verifyClass
from zope.interface import implements
from zope.app import zapi
from zope.app.intid.interfaces import IIntIds

from cybertools.relation.interfaces import IDyadicRelation, ITriadicRelation
from cybertools.relation import DyadicRelation, TriadicRelation
from cybertools.relation.interfaces import IRelationsRegistry
from cybertools.relation.registry import RelationsRegistry


class IntIdsStub:
    """A testing stub (mock utility) for IntIds."""
    implements(IIntIds)

    def __init__(self):
        self.objs = []

    def getObject(self, uid):
        return self.objs[uid]

    def getId(self, ob):
        if ob not in self.objs:
            self.objs.append(ob)
        return self.objs.index(ob)


class TestRelation(unittest.TestCase):
    "Basic tests for the relation package."

    def testInterfaces(self):
        self.assert_(IDyadicRelation.providedBy(DyadicRelation(None, None)),
            'Interface IDyadicRelation is not implemented by class DyadicRelation.')
        verifyClass(IDyadicRelation, DyadicRelation)
        self.assert_(ITriadicRelation.providedBy(TriadicRelation(None, None, None)),
             'Interface ITriadicRelation is not implemented by class TriadicRelation.')
        verifyClass(ITriadicRelation, TriadicRelation)
        self.assert_(IRelationsRegistry.providedBy(RelationsRegistry()),
            'Interface IRelationsRegistry is not implemented by class RelationsRegistry.')
        verifyClass(IRelationsRegistry, RelationsRegistry)


def test_suite():
    return unittest.TestSuite((
                unittest.makeSuite(TestRelation),
                DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
