#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
Basic classes for a complex template structures.

$Id$
"""

from zope.interface import implements

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.schema.interfaces import ISchema, IFormState
from cybertools.util.jeep import Jeep


class Schema(Template):

    implements(ISchema)

    name = u''
    manager = None

    def __init__(self, *fields, **kw):
        name = kw.get('name', None)
        if name is not None:
            self.name = name
        manager = kw.get('manager', None)
        if manager is not None:
            self.manager = self.__parent__ = manager
        super(Schema, self).__init__()
        for f in fields:
            self.components.append(f)

    @property
    def fields(self):
        return self.components

    @property
    def __name__(self):
        return self.name

    def getManager(self):
        return self.manager


class FormState(object):

    implements(IFormState)

    def __init__(self, fieldInstances=[], changed=False, severity=0):
        self.fieldInstances = Jeep(fieldInstances)
        self.changed = changed
        self.severity = severity


class FormError(object):

    def __init__(self, title, description=None, severity=5):
        self.title = title
        self.description = description or title
        self.severity = severity

    def __str__(self):
        return self.title


formErrors = dict(
    required_missing=FormError(u'Missing data for required field',
        u'Please enter data for required field.'),
    invalid_number=FormError(u'Invalid number',
        u'Please enter a number, only digits allowed.'),
)
