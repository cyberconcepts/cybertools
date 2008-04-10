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
Building flexible hierarchical object structures with XML-like
elements.

$Id$
"""

from cybertools.util.jeep import Jeep

_not_found = object()


class Element(dict):

    typeName = 'Element'
    posArgs = ('name',)

    def __init__(self, namespace, name, collection=None, parent=None):
        self.namespace = namespace
        self.name = name
        self.collection = collection
        self.parent = parent
        self.children = Jeep()

    def __call__(self, *args, **kw):
        elem = self.__class__(self.namespace, '')
        for idx, v in enumerate(args):
            if idx < len(self.posArgs):
                elem[self.posArgs[idx]] = v
        for k, v in kw.items():
            elem[k] = v
        elem.name = elem.get('name')
        if not elem.name:
            elem.name = self.name
        if self.collection is not None:
            self.collection.append(elem)
        return elem

    def __getitem__(self, key):
        if isinstance(key, (list, tuple)):
            return tuple(self[k] for k in key)
        elif isinstance(key, Element):
            self.children.append(key)
            return key
        elif isinstance(key, (int, long, basestring)):
            return self.children[key]
        else:
            raise KeyError(key)

    def __getattr__(self, key):
        result = self.get(key, _not_found)
        if result is _not_found:
            raise AttributeError(key)
        return result

    def __iter__(self):
        return iter(self.children)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s '%s'>" % (self.typeName, self.name)


class AutoElement(Element):

    typeName = 'AutoElement'

    def __call__(self, *args, **kw):
        if self.collection is None:
            elem = self
        else:
            elem = self.__class__(self.namespace, '')
            self.collection.append(elem)
        for idx, v in enumerate(args):
            if idx < len(self.posArgs):
                elem[self.posArgs[idx]] = v
        for k, v in kw.items():
            elem[k] = v
        elem.name = elem.get('name')
        if not elem.name:
            elem.name = self.name
        return elem

    def __getattr__(self, key):
        result = self.get(key, _not_found)
        if result is _not_found:
            result = self.__class__(self.namespace, key, parent=self)
            self[key] = result
        return result

    def __getitem__(self, key):
        try:
            return super(AutoElement, self).__getitem__(key)
        except KeyError:
            if isinstance(key, basestring):
                result = self.__class__(self.namespace, key, parent=self)
                self.children[key] = result
                return result
            else:
                raise KeyError(key)
