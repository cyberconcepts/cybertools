#! /usr/bin/python

"""
Tests for the 'cybertools.organize' package.

$Id$
"""

import unittest, doctest
from zope import component
from zope.testing.doctestunit import DocFileSuite
from cybertools.composer.schema import client, field, instance
from cybertools.organize.party import Person
from cybertools.organize import service


class TestParty(unittest.TestCase):
    "Basic tests for the party module."

    def testBasicStuff(self):
        p = Person('Meier', 'Hans')
        self.assertEqual('Hans', p.firstName)
        self.assertEqual('Meier', p.lastName)


def setUp(site):
    component.provideAdapter(client.ClientFactory)
    component.provideAdapter(instance.ClientInstance)
    component.provideAdapter(instance.ClientInstanceEditor, name='editor')
    component.provideAdapter(field.FieldInstance)
    component.provideAdapter(field.NumberFieldInstance, name='number')
    component.provideAdapter(field.EmailFieldInstance, name='email')
    #component.provideAdapter(field.DropdownFieldInstance, name='dropdown')
    component.provideAdapter(service.StatefulRegistration)


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(TestParty),
        DocFileSuite('README.txt', optionflags=flags),
        DocFileSuite('formmanager.txt', optionflags=flags),
        DocFileSuite('servicemanager.txt', optionflags=flags),
        DocFileSuite('work.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
