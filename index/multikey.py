#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
Dictionaries with multiple keys.

$Id$
"""

_not_found = object()
_default = object()

class MultiKeyDict(dict):

    def __init__(self, **kw):
        super(MultiKeyDict, self).__init__(**kw)
        self.singleKeyDict = {}

    def __setitem__(self, key, value):
        assert type(key) is tuple
        super(MultiKeyDict, self).__setitem__(key, value)
        for n, k in enumerate(key):
            if k:
                entry = self.singleKeyDict.setdefault((n, k), [])
                if value not in entry:
                    entry.append((key, value))

    def __getitem__(self, key):
        r = self.get(key, _default)
        if r is _default:
            raise KeyError(key)
        return r

    def get(self, key, default=None):
        assert type(key) is tuple
        kl = list(key)
        while kl:
            r = super(MultiKeyDict, self).get(tuple(kl), _not_found)
            if r is not _not_found:
                return r
            kl.pop()
        return default

    def get(self, key, default=None):
        assert type(key) is tuple
        firstTry = super(MultiKeyDict, self).get(key, _not_found)
        # fast return for full match:
        if firstTry is not _not_found:
            return firstTry
        collector = {}
        for n, k in enumerate(key):
            rList = self.singleKeyDict.get((n, k), [])
            for r in rList:
                skip = False
                for nx, kx in enumerate(r[0]):
                    if kx and kx != key[nx]: # if stored key elements are present
                        skip = True          # they must match
                        break
                if skip:
                    continue
                entry = collector.setdefault(r[1], [])
                entry.append(n)
        if not collector:
            return default
        #print 'collector', collector
        results = sorted((-len(value), value, o) for o, value in collector.items())
        #print 'sorted', results
        return results[0][2]

