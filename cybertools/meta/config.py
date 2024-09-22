# cybertools.meta.config

""" Basic implementations for configuration options
"""

import os
from zope.interface import implementer

from cybertools.meta.element import Element
from cybertools.meta.interfaces import IOptions, IConfigurator
from cybertools.meta.namespace import AutoNamespace, Executor, ExecutionError


@implementer(IOptions)
class Options(AutoNamespace):

    def __call__(self, key, default=None):
        value = self
        for part in key.split('.'):
            value = getattr(value, part, None)
        if isinstance(value, Element):
            value = default
        return value


class GlobalOptions(Options):

    _filename = None
    _lastChange = None

    def __call__(self, key, default=None):
        if self._filename is not None:
            fn = self._filename
            if os.path.exists(fn):
                modified = os.path.getmtime(fn)
                if self._lastChange is None or self._lastChange < modified:
                    Configurator(self).load(file=fn)
                    self._lastChange = modified
        return super(GlobalOptions, self).__call__(key, default)


@implementer(IConfigurator)
class Configurator(object):

    def __init__(self, context):
        self.context = context

    def load(self, text=None, file=None):
        if file is not None:
            if hasattr(file, 'read'):
                text = file.read()
            else:   # must be a file name
                f = open(file, 'r')
                text = f.read()
                f.close()
        result = Executor(self.context).execute(text)
        if result:
            raise ExecutionError('\n' + result)

    def dump(self, file=None):
        text = str(options)
        if file is not None:
            if hasattr(file, 'write'):
                file.write(text)
            else:   # must be a file name
                f = open(file, 'w')
                f.write(text)
                f.close()
        return text

