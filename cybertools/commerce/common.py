#-*- coding: UTF-8 -*-
# cybertools.commerce.common

""" Common functionality.
"""

from zope import component
from zope.intid.interfaces import IIntIds


class ContainerAttribute(object):

    def __init__(self, factory, idAttr='name'):
        self.factory = factory
        self.idAttr = idAttr
        self.data = {}

    def create(self, id, **kw):
        if self.idAttr not in kw:
            kw[self.idAttr] = id
        obj = self.factory(id)
        for k, v in kw.items():
            setattr(obj, k, v)
        self.data[id] = obj
        component.getUtility(IIntIds).register(obj)
        return obj

    def remove(self, id):
        component.getUtility(IIntIds).unregister(self.data[id])
        del self.data[id]

    def get(self, id, default=None):
        return self.data.get(id, default)

    def __iter__(self):
        return iter(self.data.values())


class RelationSet(object):

    def __init__(self, parent, attributeName=None):
        self.parent = parent
        self.attributeName = attributeName
        self.data = {}

    def add(self, related):
        self.data[related.name] = related
        if self.attributeName:
            value = getattr(related, self.attributeName)
            if isinstance(value, RelationSet):
                relatedData = value.data
                relatedData[self.parent.name] = self.parent
            else:
                setattr(related, self.attributeName, self.parent)

    def remove(self, related):
        name = related.name
        del self.data[name]
        if self.attributeName:
            value = getattr(related, self.attributeName)
            if isinstance(value, RelationSet):
                relatedData = value.data
                del relatedData[self.parent.name]
            else:
                setattr(related, self.attributeName, None)

    def __iter__(self):
        for obj in self.data.values():
            yield obj


class Relation(object):

    def __init__(self, name, otherName):
        self.name = name
        self.otherName = otherName

    def __get__(self, inst, class_=None):
        if inst is None:
            return self
        return getattr(inst, self.name)

    def __set__(self, inst, value):
        existing = getattr(inst, self.name, None)
        if existing is not None:
            other = getattr(existing, self.otherName).data
            for k, v in other.items():
                if v != inst:
                    del other[k]
        if value is not None:
            other = getattr(value, self.otherName).data
            other[inst.name] = inst
        setattr(inst, self.name, value)


class BaseObject(object):

    collection = RelationSet


class FloatValue(float):
    # TODO: rename to CurrencyValue

    def __nonzero__(self):
        return True  # even when value is 0.0

    def __init__(self, value, decimals=2, currency=u'€'):
        self.decimals = decimals
        self.currency = currency

    def __str__(self):
        format = '%%.%if' % self.decimals
        value = (format % self).replace('.', ',')
        if self.currency:
            value = value + ' ' + self.currency
        return value

    def rawValue(self):
        return float(self)

    def rawFormatted(self):
        format = '%%.%if' % self.decimals
        return (format % self)


# utility functions

def getUidForObject(obj, intIds=None):
    if intIds is None:
        intIds = component.getUtility(IIntIds)
    return str(intIds.getId(obj))

def getObjectForUid(uid, intIds=None):
    if intIds is None:
        intIds = component.getUtility(IIntIds)
    if isinstance(uid, str) and isdigit(uid):
        uid = int(uid)
    return intIds.getObject(uid)

