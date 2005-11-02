# $Id$

import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import ztapi
from zope.interface.verify import verifyClass
from zope.app import zapi

from cybertools.relation.interfaces import IDyadicRelation, ITriadicRelation
from cybertools.relation import DyadicRelation, TriadicRelation
from cybertools.relation.interfaces import IRelationsRegistry
from cybertools.relation.registry import RelationsRegistry


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
