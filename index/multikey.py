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

class MultiKeyDict(dict):

    def __init__(self, keylen=None, **kw):
        super(MultiKeyDict, self).__init__(**kw)
        self.submapping = {}
        self.keylen = keylen

    def __setitem__(self, key, value):
        assert type(key) is tuple
        if self.keylen is None:
            self.keylen = len(key)
        assert len(key) == self.keylen
        k0 = key[0]
        if len(key) > 1:
            sub = self.submapping.setdefault(k0, MultiKeyDict(self.keylen-1))
            sub[key[1:]] = value
        super(MultiKeyDict, self).__setitem__(k0, value)

    def __getitem__(self, key):
        r = self.get(key, _not_found)
        if r is _not_found:
            raise KeyError(key)
        return r

    def get(self, key, default=None):
        assert type(key) is tuple
        assert len(key) == self.keylen
        k0 = key[0]
        rsub = _not_found
        r0 = super(MultiKeyDict, self).get(k0, _not_found)
        if r0 is _not_found:
            r0 = self.getFallback(k0)
        if r0 is _not_found:
            return default
        if len(key) > 1:
            sub = self.submapping.get(k0, _not_found)
            if sub is _not_found:
                sub = self.getSubmappingFallback(key)
            if sub is _not_found:
                rsub = _not_found
            else:
                rsub = sub.get(key[1:], _not_found)
                if rsub is _not_found:
                    return default
        result = rsub is _not_found and r0 or rsub
        return result is _not_found and default or result

    def getFallback(self, key):
        return super(MultiKeyDict, self).get(None, _not_found)

    def getSubmappingFallback(self, key):
        return self.submapping.get(None, _not_found)

    def __repr__(self):
        return ('<MultiKeyDict %s; submapping: %s>'
                % (super(MultiKeyDict, self).__repr__(), `self.submapping`))

