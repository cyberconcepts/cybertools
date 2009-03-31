#-*- coding: UTF-8 -*-
#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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
Common functionality.

$Id$
"""

from zope.app.intid.interfaces import IIntIds
from zope import component


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

    def __init__(self, value, decimals=2, currency=u'€'):
        self.decimals = decimals
        self.currency = currency

    def __str__(self):
        format = '%%.%if' % self.decimals
        value = (format % self).replace('.', ',')
        if self.currency:
            value = value + ' ' + self.currency
        return value


# utility functions

def getUidForObject(obj, intIds=None):
    if intIds is None:
        intIds = component.getUtility(IIntIds)
    return intIds.getId(obj)

def getObjectForUid(uid, intIds=None):
    if intIds is None:
        intIds = component.getUtility(IIntIds)
    return intIds.getObject(uid)

