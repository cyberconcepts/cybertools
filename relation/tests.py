# $Id$

import unittest
from zope.app.testing import ztapi
from zope.interface.verify import verifyClass
from zope.interface import implements
from zope.intid.interfaces import IIntIds

from cybertools.relation.interfaces import IDyadicRelation, ITriadicRelation
from cybertools.relation.interfaces import IRelation, IPredicate
from cybertools.relation import Relation, DyadicRelation, TriadicRelation
from cybertools.relation.interfaces import IRelationRegistry


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


class TestRelation(unittest.TestCase):
    "Basic tests for the relation package."

    def testInterfaces(self):
        verifyClass(IPredicate, Relation)
        verifyClass(IRelation, Relation)
        self.assert_(IDyadicRelation.providedBy(DyadicRelation(None, None)),
            'Interface IDyadicRelation is not implemented by class DyadicRelation.')
        verifyClass(IDyadicRelation, DyadicRelation)
        self.assert_(ITriadicRelation.providedBy(TriadicRelation(None, None, None)),
             'Interface ITriadicRelation is not implemented by class TriadicRelation.')
        verifyClass(ITriadicRelation, TriadicRelation)
        # avoid dependency on import:
        from cybertools.relation.registry import RelationRegistry
        self.assert_(IRelationRegistry.providedBy(RelationRegistry()),
            'Interface IRelationRegistry is not implemented by class RelationRegistry.')
        verifyClass(IRelationRegistry, RelationRegistry)


def test_suite():
    return unittest.TestSuite((
                unittest.makeSuite(TestRelation),
                doctest.DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
