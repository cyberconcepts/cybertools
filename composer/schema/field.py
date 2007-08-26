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
Schema fields and related classes.

$Id$
"""

from zope.interface import implements
from zope import schema

from cybertools.composer.base import Component
from cybertools.composer.schema.interfaces import IField, IFieldState
from cybertools.util.format import toStr, toUnicode


class Field(Component):

    implements(IField)

    required = False

    def __init__(self, name, title=None, renderFactory=None, **kw):
        assert name
        self.__name__ = name
        title = title or u''
        self.renderFactory = renderFactory  # use for rendering field content
        super(Field, self).__init__(title, __name__=name, **kw)
        self.title = title
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def name(self):
        return self.__name__

    #@property
    #def title(self):
    #    return self.title or self.name

    def getTitleValue(self):
        return self.title or self.name

    def marshallValue(self, value):
        return toStr(value)

    def displayValue(self, value):
        return toStr(value)

    def unmarshallValue(self, strValue):
        return toUnicode(strValue) or u''

    def validateValue(self, value):
        errors = []
        severity = 0
        if not value and self.required:
            errors.append('required_missing')
            severity = 5
        return FieldState(self.name, errors, severity)


class FieldState(object):

    implements(IFieldState)

    def __init__(self, name, errors=[], severity=0, change=None):
        self.name = self.__name__ = name
        self.errors = errors
        self.severity = severity
        self.change = change

