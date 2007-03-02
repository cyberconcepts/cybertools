#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
A general purpose (thus 'Jeep') class that provides most of the interfaces
of sequences and dictionaries and in addition allows attribute access to
the dictionary entries.

$Id$
"""

_notfound = object()

class Jeep(object):

    _attributes = ('_sequence',)

    def __init__(self, init=None):
        self._sequence = []
        if init is not None:
            for attr, value in init:
                setattr(self, attr, value)

    def __iter__(self):
        for key in self._sequence:
            yield key

    def __setattr__(self, attr, value):
        if not attr in self._attributes:
            if getattr(self, attr, _notfound) is _notfound:
                self._sequence.append(attr)
        object.__setattr__(self, attr, value)

    def __getitem__(self, key):
        if type(key) is int:
            return getattr(self, self._sequence[key])
        value = getattr(self, key, _notfound)
        if value is _notfound:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def keys(self):
        return list(self)

    def values(self):
        return [self[k] for k in self]

    def items(self):
        return [(k, self[k]) for k in self]

    def get(self, key, default=None):
        return getattr(self, key, default)
