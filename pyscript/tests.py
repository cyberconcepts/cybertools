##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests for Python Page

$Id$
"""

import unittest, doctest
from zope import component
from zope.interface import implements
from zope.location.traversing import LocationPhysicallyLocatable
from zope.testing.doctestunit import DocFileSuite
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
    suites = [DocFileSuite('README.txt', optionflags=flags,
              setUp=setUp, tearDown=placelesssetup.tearDown)]
    if HAS_R:
        suites.append(DocFileSuite('rstat.txt', optionflags=flags,
                      setUp=setUp, tearDown=placelesssetup.tearDown))
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    unittest.main()
