# cybertools.util.adapter

""" A simple adapter framework.
"""


class AdapterFactory(object):

    def __init__(self):
        self._registry = {}

    def register(self, adapter, adapted, name=''):
        """ Register `adapter` class for objects of class `adapted`.
            Optionally associate the adapter with a `name`; thus there
            can be more than one adapter for one class.
        """
        self._registry[(adapted, name)] = adapter

    def queryAdapter(self, obj, name):
        class_ = type(obj) is type and obj or obj.__class__
        adapter = None
        while adapter is None and class_:
            adapter = self._registry.get((class_, name))
            if adapter is None:
                bases = class_.__bases__
                class_ = bases and bases[0] or None
        return adapter

    def __call__(self, obj, name=''):
        """ Return an adapter instance on `obj` with the `name` given.
            if obj is a class use this class for the adapter lookup, else
            use obj's class.
            If there isn't an adapter directly for the class
            check also for its base classes.
        """
        adapter = self.queryAdapter(obj, name)
        if adapter is None:
            return None
        return adapter(obj)


# self-registering adapters

adapters = AdapterFactory()


class AdapterType(type):
    """ To be used as metaclass for self-registering adapters.
    """

    def __init__(cls, name, bases, cdict):
        super(AdapterType, cls).__init__(name, bases, cdict)
        info = list(cdict.get('__adapterinfo__', (adapters, object, '')))
        if len(info) < 2:
            info.append(object)
        if len(info) < 3:
            info.append('')
        factory, adapted, name = info
        factory.register(cls, adapted, name)


class AdapterBase(object, metaclass=AdapterType):

    pass

