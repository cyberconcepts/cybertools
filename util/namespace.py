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
Special namespaces for execution of Python code, e.g. for implementing
configuration or export/import formats, or providing a restricted Python
for scripts or an interactive interpreter.

$Id$
"""

import traceback

_not_found = object()


class BaseNamespace(dict):

    builtins = 'dir', 'output'

    def __init__(self, *args, **kw):
        super(BaseNamespace, self).__init__(*args, **kw)
        self['__builtins__'] = {}
        for key in self.builtins:
            self[key] = getattr(self, key)

    def output(self, value):
        print value

    def dir(self, obj=None):
        if obj is None:
            return dir(self)
        return dir(obj)

    def __getitem__(self, key):
        result = self.get(key, _not_found)
        if result is _not_found:
            raise NameError(key)
        return result

    def __getattr__(self, key):
        result = self.get(key, _not_found)
        if result is _not_found:
            raise AttributeError(key)
        return result


class Symbol(object):

    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Symbol '%s'>" % self.name


class AutoNamespace(BaseNamespace):

    symbolFactory = Symbol

    def __getitem__(self, key):
        result = self.get(key, _not_found)
        if result is _not_found:
            result = getattr(self, key, _not_found)
            if result is _not_found:
                sym = Symbol(self, key)
                self[key] = sym
                return sym
        return result
