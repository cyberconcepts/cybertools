#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
Implementation of report field definitions.

$Id$
"""

from datetime import datetime
from time import strptime, strftime
from zope.interface import implements
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope import component
from zope.i18n.locales import locales

from cybertools.composer.base import Component
from cybertools.composer.report.interfaces import IField
from cybertools.composer.report.interfaces import fieldTypes


class Field(Component):

    implements(IField)

    vocabulary = None
    default = None
    instance_name = None
    storeData = True
    renderer = 'standard'

    executionSteps = ['query', 'sort', 'output']

    def __init__(self, name, title=None, fieldType='textline', **kw):
        assert name
        self.__name__ = name
        title = title or name
        self.fieldType = fieldType
        super(Field, self).__init__(title, __name__=name, **kw)
        self.title = title
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def name(self):
        return self.__name__

    def getRawValue(self, row):
        return getattr(row.context, self.name)

    def getValue(self, row):
        value = self.getRawValue(row)
        if value is None:
            return u''
        if isinstance(value, basestring):
            return value
        return getattr(value, 'title', str(value))

    def getSortValue(self, row):
        # TODO: consider 'descending' flag, use raw value instead of formatted one
        return self.getValue(row)


label = Field('label', u'Label',
                u'A short text that identifies a row for humans.')

