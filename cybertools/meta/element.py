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

from cStringIO import StringIO

from cybertools.util.jeep import Jeep

_not_found = object()


class Element(dict):

    typeName = 'Element'
    posArgs = ('__name__',)
    realAttributes = ('namespace', '__name__', 'factory', 'parent', 'children')

    def __init__(self, namespace, name, factory=None, parent=None):
        self.namespace = namespace
        self.__name__ = name
        self.parent = parent
        self.factory = factory
        self.children = Jeep()

    def __call__(self, *args, **kw):
        for idx, v in enumerate(args):
            if isinstance(v, Element):
                self[v.__name__] = v
            elif idx < len(self.posArgs):
                self[self.posArgs[idx]] = v
        for k, v in kw.items():
            self[k] = v
        return self

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
            result = self.children.get(key, _not_found)
            if result is _not_found:
                raise AttributeError(key)
        return result

    def __setattr__(self, key, value):
        if key in self.realAttributes or key.startswith('_'):
            super(Element, self).__setattr__(key, value)
        else:
            self[key] = value

    def __iter__(self):
        return iter(self.children)

    def __str__(self):
        return self.__name__

    def __repr__(self):
        return "<%s '%s'>" % (self.typeName, self.__name__)


class ElementFactory(object):

    elementClass = Element

    def __init__(self, namespace, name):
        self.namespace = namespace
        self.__name__ = name
        self.instances = []

    def __call__(self, *args, **kw):
        elem = self.elementClass(self.namespace, '', factory=self)
        for idx, v in enumerate(args):
            if idx < len(elem.posArgs):
                elem[elem.posArgs[idx]] = v
        for k, v in kw.items():
            elem[k] = v
        elem.__name__ = elem.get('__name__')
        if not elem.__name__:
            elem.__name__ = self.__name__
        self.instances.append(elem)
        return elem


class AutoElement(Element):

    typeName = 'AutoElement'

    def __getattr__(self, key):
        if key.startswith('_'):     # no auto-creation for special attributes
            raise AttributeError(key)
        result = self.get(key, _not_found)
        if result is _not_found:
            result = self.children.get(key, _not_found)
            if result is _not_found:
                result = self.__class__(self.namespace, key, parent=self)
                self.children[key] = result
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

    def __str__(self):
        out = StringIO()
        for v in self.children:
            out.write('%s.%s\n' % (self.__name__, v))
        if self or not self.children:
            out.write(self.__name__)
        if self:
            out.write('(')
            out.write(', '.join('%s=%r' % (k, v) for k, v in self.items()))
            out.write(')')
        return out.getvalue()

