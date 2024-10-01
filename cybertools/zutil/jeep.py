# cybertools.zutil.jeep

""" A general purpose (thus 'Jeep') class that provides most of the interfaces
of sequences and dictionaries and in addition allows attribute access to
the dictionary entries.

This is the Zope-based persistent variant of the Jeep class.
"""

from persistent import Persistent
from persistent.list import PersistentList
from BTrees.OOBTree import OOBTree
from zope.app.container.interfaces import IContainer
from zope.interface import implementer

_notfound = object()
_nodefault = object()


@implementer(IContainer)
class Jeep(Persistent):

    _attributes = ('_sequence', '_mapping')

    def __init__(self, seq=[]):
        sequence = self._sequence = PersistentList()
        mapping = self._mapping = OOBTree()
        for attr, value in seq:
            sequence.append(attr)
            mapping[attr] = value

    def __len__(self):
        return len(self._sequence)

    def __iter__(self):
        for key in self._sequence:
            yield self[key]

    def __getattr__(self, attr, default=_nodefault):
        value = self._mapping.get(attr, _notfound)
        if value is _notfound:
            if default is _nodefault:
                raise AttributeError(attr)
            else:
                return default
        return value

    def __setattr__(self, attr, value):
        if attr in self._attributes:
            super(Jeep, self).__setattr__(attr, value)
        else:
            if getattr(self, attr, _notfound) is _notfound:
                self._sequence.append(attr)
            self._mapping[attr] = value

    def __delattr__(self, attr):
        del self._sequence[self.index(attr)]
        del self._mapping[attr]

    def __getitem__(self, key):
        if isinstance(key, int):
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

    has_key = __contains__

    def keys(self):
        return [key for key in self._sequence]

    def values(self):
        return list(self)

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
        self._mapping[key] = obj

    def pop(self, key=-1):
        value = self[key]
        if isinstance(key, int):
            key = self._sequence[key]
        delattr(self, key)
        return value

