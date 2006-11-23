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

class MultiKeyDict(object):

    def __init__(self, keylen=None):
        self.keylen = keylen
        self.mapping = {}

    def __setitem__(self, key, value):
        assert type(key) is tuple
        assert len(key) > 0
        if self.keylen is None:
            self.keylen = len(key)
        assert len(key) == self.keylen
        mapping = self.mapping
        for n, k in enumerate(key):
            if n == self.keylen - 1:
                mapping[k] = value
            else:
                mapping = mapping.setdefault(k, {})

    def __getitem__(self, key):
        r = self.get(key, _not_found)
        if r is _not_found:
            raise KeyError(key)
        return r

    def get(self, key, default=None):
        assert type(key) is tuple
        assert len(key) == self.keylen
        mapping = self.mapping
        for n, k in enumerate(key):
            entry = mapping.get(k, _not_found)
            if entry == _not_found:
                entry = self._fallback(mapping, k)
            if entry == _not_found:
                return default
            mapping = entry
        return entry

    def _fallback(self, mapping, key):
        return mapping.get(None, _not_found)

