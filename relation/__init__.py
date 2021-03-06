# -*- coding: UTF-8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
#
#  Copyright (c) 2013 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
The relation package provides all you need for setting up dyadic and
triadic relations.
"""

from persistent import Persistent
from zope.interface import implements
from interfaces import IPredicate
from interfaces import IRelation, IDyadicRelation, ITriadicRelation
from interfaces import IRelatable

class Relation(Persistent):

    implements(IPredicate, IRelation)

    order = 0
    relevance = 1.0
    fallback = None

    @classmethod
    def getPredicateName(cls):
        return '%s.%s' % (cls.__module__, cls.__name__)

    @property
    def ident(self):
        return self.getPredicateName()

    def validate(self, registry=None):
        return True

    def checkRelatable(self, *objects):
        for obj in objects:
            if obj is not None and not IRelatable.providedBy(obj):
                raise(ValueError, 'Objects to be used in relations '
                        'must provide the IRelatable interface.')


class DyadicRelation(Relation):

    implements(IDyadicRelation)

    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.checkRelatable(first, second)


class TriadicRelation(Relation):

    implements(ITriadicRelation)

    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third
        self.checkRelatable(first, second, third)

