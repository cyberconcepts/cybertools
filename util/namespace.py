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

from cybertools.util.jeep import Jeep

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


class Element(object):

    posArgs = ('name',)

    def __init__(self, namespace, name, collection=None, parent=None):
        self.namespace = namespace
        self.name = name
        self.collection = collection
        self.parent = parent
        self.subElements = Jeep()

    def __call__(self, *args, **kw):
        elem = self.__class__(self.namespace, '', parent=self)
        for idx, v in enumerate(args):
            if idx < len(self.posArgs):
                setattr(elem, self.posArgs[idx], v)
        for k, v in kw.items():
            setattr(elem, k, v)
        if not elem.name:
            elem.name = self.name
        if self.collection is not None:
            self.collection.append(elem)
        return elem

    def __getitem__(self, key):
        if isinstance(key, (list, tuple)):
            return tuple(self[k] for k in key)
        elif isinstance(key, Element):
            self.subElements.append(key)
            return key
        elif isinstance(key, (int, long, basestring)):
            return self.subElements[key]
        else:
            print '*** Error', key

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Element '%s'>" % self.name


class AutoNamespace(BaseNamespace):

    elementFactory = Element

    def __getitem__(self, key):
        result = self.get(key, _not_found)
        if result is _not_found:
            result = getattr(self, key, _not_found)
            if result is _not_found:
                elem = Element(self, key)
                self[key] = elem
                return elem
        return result


class Executor(object):

    def __init__(self, namespace):
        self.namespace = namespace

    def execute(self, text):
        error = ''
        try:
            exec text in self.namespace
        except:
            error = traceback.format_exc()
        return error


class Evaluator(Executor):

    def __init__(self, namespace, allowExec=False):
        self.namespace = namespace
        self.allowExec = allowExec

    def evaluate(self, text):
        """ Evaluate the text as a Python expression given and return the
            result. If the text is not an expression try to execute it
            as a statement (resulting in a None value).

            The return value is a tuple with the evaluation result and
            an error traceback if there was an error.
        """
        if self.allowExec:
            return self.evalutateOrExecute(text)
        result = None
        error = ''
        try:
            result = eval(text, self.namespace)
        except:
            error = traceback.format_exc()
        return result, error

    def evalutateOrExecute(self, text):
        result = None
        error = ''
        try:
            result = eval(text, self.namespace)
        except SyntaxError:
            error = self.execute(text)
        except:
            error = traceback.format_exc()
        return result, error
