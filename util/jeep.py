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

    def __init__(self, seq=[]):
        sequence = self._sequence = []
        for attr, value in seq:
            sequence.append(attr)
            object.__setattr__(self, attr, value)

    def __len__(self):
        return len(self._sequence)

    def __iter__(self):
        for key in self._sequence:
            yield self[key]

    def __setattr__(self, attr, value):
        if not attr in self._attributes:
            if getattr(self, attr, _notfound) is _notfound:
                self._sequence.append(attr)
        super(Jeep, self).__setattr__(attr, value)

    def __delattr__(self, attr):
        del self._sequence[self.index(attr)]
        super(Jeep, self).__delattr__(attr)

    def __getitem__(self, key):
        if type(key) in (int, long):
            return getattr(self, self._sequence[key])
        value = getattr(self, key, _notfound)
        if value is _notfound:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __contains__(self, key):
        return getattr(self, key, _notfound) is not _notfound

    def keys(self):
        return [key for key in self._sequence]

    def values(self):
        return list(self)
        return [self[k] for k in self]

    def items(self):
        return [(k, self[k]) for k in self._sequence]

    def get(self, key, default=None):
        return getattr(self, key, default)

    def index(self, key):
        return self._sequence.index(key)

    def append(self, obj):
        self.insert(len(self), obj)

    def insert(self, idx, obj):
        key = getattr(obj, '__name__', getattr(obj, 'name', _notfound))
        if key is _notfound:
            raise AttributeError("No name attribute present")
        if key in self:
            raise ValueError("Object already present")
        self._sequence.insert(idx, key)
        object.__setattr__(self, key, obj)

    def pop(self, key=-1):
        value = self[key]
        if type(key) in (int, long):
            key = self._sequence[key]
        delattr(self, key)
        return value

    def find(self, obj):
        if isinstance(obj, basestring):
            key = obj
        else:
            key = getattr(obj, '__name__', getattr(obj, 'name', _notfound))
            if key is _notfound:
                raise AttributeError("No name attribute present")
        if key in self:
            return self._sequence.index(key)
        else:
            return -1

    def index(self, obj):
        idx = self.find(obj)
        if idx < 0:
            raise ValueError('list.index(x): x not in list')
        return idx


class Term(object):
    """ A simple name/title association that may be put in a jeep object.
    """

    def __init__(self, name, title, **kw):
        self.name = self.__name__ = name
        self.title = title
        for k, v in kw.items():
            setattr(self, k, v)

