"""Tests for pyscript

Based on Zope Python Page.

$Id$
"""

import unittest, doctest
from zope import component
from zope.interface import implements
from zope.location.traversing import LocationPhysicallyLocatable
from zope.traversing.interfaces import IContainmentRoot
from zope.traversing.interfaces import IPhysicallyLocatable
from zope.traversing.adapters import RootPhysicallyLocatable
from zope.app.container.contained import Contained
from zope.app.testing import placelesssetup
from cybertools.pyscript.script import ScriptContainer, HAS_R


class Root(ScriptContainer, Contained):
    implements(IContainmentRoot)

    __parent__ = None
    __name__ = 'root'


def setUp(test):
    placelesssetup.setUp()
    component.provideAdapter(LocationPhysicallyLocatable)
    component.provideAdapter(RootPhysicallyLocatable)


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    suites = [doctest.DocFileSuite('README.txt', optionflags=flags,
              setUp=setUp, tearDown=placelesssetup.tearDown)]
    if HAS_R:
        suites.append(doctest.DocFileSuite('rstat.txt', optionflags=flags,
                      setUp=setUp, tearDown=placelesssetup.tearDown))
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    unittest.main()
