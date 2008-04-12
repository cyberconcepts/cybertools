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

from cybertools.meta.element import Element, AutoElement
from cybertools.util.jeep import Jeep

_not_found = object()


class BaseNamespace(dict):

    builtins = '__builtins__', 'dir', 'output'

    def __init__(self, *args, **kw):
        self.__builtins__ = {}
        super(BaseNamespace, self).__init__(*args, **kw)
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

    def __str__(self):
        def result():
            for k, v in self.items():
                if k not in self.builtins:
                    if isinstance(v, Element):
                        yield str(v)
                    else:
                        yield '%s=%r' % (k, v)
        return '\n'.join(list(result()))

    __repr__ = object.__repr__


class AutoNamespace(BaseNamespace):

    elementFactory = AutoElement

    def __getitem__(self, key):
        result = self.get(key, _not_found)
        if result is _not_found:
            result = self.elementFactory(self, key)
            self[key] = result
        return result

    def __getattr__(self, key):
        if key.startswith('_'):     # no auto-creation for special attributes
            raise AttributeError(key)
        return self[key]


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


class ExecutionError(ValueError):

    pass
