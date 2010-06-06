#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
_undefined = object()

class Jeep(object):

    _attributes = ('_sequence',)

    def __init__(self, seq=[], **kw):
        if isinstance(seq, Jeep):
            self._sequence = list(seq.keys())
            for key, value in seq.items():
                object.__setattr__(self, key, value)
        else:
            sequence = self._sequence = []
            for item in seq:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    attr, value = item
                    sequence.append(attr)
                    object.__setattr__(self, attr, value)
                else:
                    self.append(item)
        for k, v in kw.items():
            self[k] = v

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
        return list(self._sequence)

    def values(self):
        return list(self)
        #return [self[k] for k in self]

    def items(self):
        return [(k, self[k]) for k in self._sequence]

    def get(self, key, default=None):
        return getattr(self, key, default)

    def setdefault(self, key, value):
        existing = self.get(key, default=_notfound)
        if existing is _notfound:
            self[key] = value
            return value
        return existing

    def append(self, obj):
        self.insert(len(self), obj)

    def extend(self, sequence):
        for obj in sequence:
            self.append(obj)

    def insert(self, idx, obj):
        key = getattr(obj, '__name__', getattr(obj, 'name', _notfound))
        if key is _notfound:
            raise AttributeError("No name attribute present")
        if key in self.keys():
            raise ValueError("Object '%s' already present" % key)
        self._sequence.insert(idx, key)
        object.__setattr__(self, key, obj)

    def update(self, mapping):
        for key, value in mapping.items():
            self[key] = value

    def pop(self, key=-1, default=_undefined):
        if type(key) in (int, long):
            key = self._sequence[key]
        if default is _undefined:
            value = self[key]
        else:
            value = self.get(key, default)
        self.remove(key)
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
            raise ValueError('list.index(x): %r not in list' % obj)
        return idx

    def remove(self, *keys):
        myKeys = self.keys()
        for key in keys:
            if key in myKeys:
                del self[key]

    def select(self, *keys):
        myKeys = self._sequence
        self._sequence = [k for k in keys if k in myKeys]
        for k in myKeys:
            if k not in keys:
                super(Jeep, self).__delattr__(k)

    def reorder(self, delta, *keys):
        self._sequence = moveByDelta(self._sequence, keys, delta)


class Term(object):
    """ A simple name/title association that may be put in a jeep object.
    """

    def __init__(self, name, title, **kw):
        self.name = self.__name__ = self.value = self.token = name
        self.title = title
        for k, v in kw.items():
            setattr(self, k, v)

    def __str__(self):
        return self.title


def moveByDelta(objs, toMove, delta):
    """ Return the list given by objs re-ordered in a way that the elements
        of toMove (which must be in the objs list) have been moved by delta.
    """
    result = [obj for obj in objs if obj not in toMove]
    if delta < 0:
        objs = list(reversed(objs))
        result.reverse()
    toMove = sorted(toMove, lambda x,y: cmp(objs.index(x), objs.index(y)))
    for element in toMove:
        newPos = min(len(result), objs.index(element) + abs(delta))
        result.insert(newPos, element)
    if delta < 0:
        result.reverse()
    return result

