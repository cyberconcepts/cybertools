# cybertools.util.config

""" Formulating configuration options.
"""


import os

from cybertools.util.jeep import Jeep


_not_found = object()


class Configurator(dict):

    filenamePrefix = 'cybertools'

    def __init__(self, *sections, **kw):
        for s in sections:
            setattr(self, s, ConfigSection(s))
        self.filename = kw.get('filename')

    def __getitem__(self, key):
        return getattr(self, key)

    def __getattr__(self, key):
        item = ConfigSection(key)
        setattr(self, key, item)
        return item

    def load(self, p=None, filename=None):
        if p is None:
            fn = self.getConfigFile(filename)
            if fn is not None:
                f = open(fn, 'r')
                p = f.read()
                f.close()
        if p is None:
            return
        exec(p, self)

    def save(self, filename=None):
        fn = self.getConfigFile(filename)
        if fn is None:
            fn = self.getDefaultConfigFile()
        if fn is not None:
            f = open(fn, 'w')
            f.write(repr(self))
            f.close()

    def __repr__(self):
        result = []
        for name, value in self.__dict__.items():
            if isinstance(value, ConfigSection):
                value.collect(name, result)
        return '\n'.join(sorted(result))

    def getConfigFile(self, filename=None):
        if filename is not None:
            self.filename = filename
        if self.filename is None:
            fn = self.getDefaultConfigFile()
            if os.path.isfile(fn):
                self.filename = fn
        return self.filename

    def getDefaultConfigFile(self):
        return os.path.join(os.path.expanduser('~'),
                            '.%s.cfg' % self.filenamePrefix)


class ConfigSection(list):

    __name__ = '???'

    def __init__(self, name=None):
        if name is not None:
            self.__name__ = name

    def __getattr__(self, attr):
        value = ConfigSection(attr)
        setattr(self, attr, value)
        return value

    def __getitem__(self, idx):
        while idx >= len(self):
            self.append(ConfigSection())
        return list.__getitem__(self, idx)

    def setdefault(self, attr, value):
        if attr not in self.__dict__:
            setattr(self, attr, value)
            return value
        return getattr(self, attr)

    def items(self):
        for name, value in self.__dict__.items():
            if isinstance(value, (str, int)):
                yield name, value

    def __call__(self, *args, **kw):
        for s in args:
            if isinstance(s, ConfigSection):
                # should we update an existing entry?
                #old = getattr(self, s.__name__, None)
                #if old is not None:  # this would have to be done recursively
                #    old.__dict__.update(s.__dict__)
                #    for elem in s:
                #        old.append(elem)
                #else:
                # or just keep the new one?
                setattr(self, s.__name__, s)
        for k, v in kw.items():
            setattr(self, k, v)
        return self

    def collect(self, ident, result):
        for idx, element in enumerate(self):
            element.collect('%s[%i]' % (ident, idx), result)
        for name, value in self.__dict__.items():
            if isinstance(value, ConfigSection):
                value.collect('%s.%s' % (ident, name), result)
            elif name != '__name__' and isinstance(value, (str, int, list, tuple)):
                result.append('%s.%s = %r' % (ident, name, value))

