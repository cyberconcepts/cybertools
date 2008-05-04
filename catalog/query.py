#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
Catalog query terms and their logical combinations.

This is mainly a simplified version of Martijn Faassen's hurry.query
(http://cheeseshop.python.org/pypi/hurry.query).

$Id$
"""

from BTrees.IFBTree import weightedIntersection, weightedUnion
from BTrees.IFBTree import difference, IFBTree, IFBucket, IFSet
from BTrees.IIBTree import IISet, union
from zope.app.intid.interfaces import IIntIds
from zope.app.catalog.catalog import ResultSet
from zope.app.catalog.field import IFieldIndex
from zope.app.catalog.text import ITextIndex
from zope.app.catalog.interfaces import ICatalog
from zope import component

from cybertools.catalog.keyword import IKeywordIndex


class Term(object):

    def __and__(self, other):
        return And(self, other)

    def __rand__(self, other):
        return And(other, self)

    def __or__(self, other):
        return Or(self, other)

    def __ror__(self, other):
        return Or(other, self)

    def __invert__(self):
        return Not(self)


class And(Term):

    def __init__(self, *terms):
        self.terms = terms

    def apply(self):
        results = []
        for term in self.terms:
            r = term.apply()
            if not r:
                # empty results
                return r
            results.append((len(r), r))
        if not results:
            # no applicable terms at all
            return IFBucket()
        results.sort()
        _, result = results.pop(0)
        for _, r in results:
            w, result = weightedIntersection(result, r)
        return result


class Or(Term):

    def __init__(self, *terms):
        self.terms = terms

    def apply(self):
        results = []
        for term in self.terms:
            r = term.apply()
            # empty results
            if not r:
                continue
            results.append(r)
        if not results:
            # no applicable terms at all
            return IFBucket()
        result = results.pop(0)
        for r in results:
            w, result = weightedUnion(result, r)
        return result


class Not(Term):

    def __init__(self, term):
        self.term = term

    def apply(self):
        return difference(self._all(), self.term.apply())

    def _all(self):
        # XXX may not work well/be efficient with extentcatalog
        # XXX not very efficient in general, better to use internal
        # IntIds datastructure but that would break abstraction..
        intids = component.getUtility(IIntIds)
        result = IFBucket()
        for uid in intids:
            result[uid] = 0
        return result


class IndexTerm(Term):

    def __init__(self, (catalog_name, index_name)):
        self.catalog_name = catalog_name
        self.index_name = index_name

    def getIndex(self):
        catalog = component.getUtility(ICatalog, self.catalog_name)
        index = catalog[self.index_name]
        return index


# field index

class FieldTerm(IndexTerm):

    def getIndex(self):
        index = super(FieldTerm, self).getIndex()
        assert IFieldIndex.providedBy(index)
        return index


class Eq(FieldTerm):

    def __init__(self, index_id, value):
        assert value is not None
        super(Eq, self).__init__(index_id)
        self.value = value

    def apply(self):
        return self.getIndex().apply((self.value, self.value))


class NotEq(FieldTerm):

    def __init__(self, index_id, not_value):
        super(NotEq, self).__init__(index_id)
        self.not_value = not_value

    def apply(self):
        index = self.getIndex()
        all = index.apply((None, None))
        r = index.apply((self.not_value, self.not_value))
        return difference(all, r)


class Between(FieldTerm):

    def __init__(self, index_id, min_value, max_value):
        super(Between, self).__init__(index_id)
        self.min_value = min_value
        self.max_value = max_value

    def apply(self):
        return self.getIndex().apply((self.min_value, self.max_value))


class Ge(Between):

    def __init__(self, index_id, min_value):
        super(Ge, self).__init__(index_id, min_value, None)


class Le(Between):

    def __init__(self, index_id, max_value):
        super(Le, self).__init__(index_id, None, max_value)


class In(FieldTerm):

    def __init__(self, index_id, values):
        assert None not in values
        super(In, self).__init__(index_id)
        self.values = values

    def apply(self):
        results = []
        index = self.getIndex()
        for value in self.values:
            r = index.apply((value, value))
            # empty results
            if not r:
                continue
            results.append(r)
        if not results:
            # no applicable terms at all
            return IFBucket()
        result = results.pop(0)
        for r in results:
            w, result = weightedUnion(result, r)
        return result


# text index

class Text(IndexTerm):

    def __init__(self, index_id, text):
        super(Text, self).__init__(index_id)
        self.text = text

    def getIndex(self):
        index = super(Text, self).getIndex()
        assert ITextIndex.providedBy(index)
        return index

    def apply(self):
        index = self.getIndex()
        return index.apply(self.text)


# keyword index

class KeywordTerm(IndexTerm):

    def __init__(self, index_id, values):
        super(KeywordTerm, self).__init__(index_id)
        self.values = values

    def getIndex(self):
        index = super(KeywordTerm, self).getIndex()
        assert IKeywordIndex.providedBy(index)
        return index


class AnyOf(KeywordTerm):

    def apply(self):
        result = self.getIndex().search(self.values, 'or')
        if isinstance(result, IFSet):
            return result
        return IFSet(result)


class AllOf(KeywordTerm):

    def apply(self):
        result = self.getIndex().search(self.values, 'and')
        if isinstance(result, IFSet):
            return result
        return IFSet(result)

