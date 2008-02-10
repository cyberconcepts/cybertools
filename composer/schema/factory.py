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
Schema factory stuff.

$Id$
"""

from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope import schema

from cybertools.composer.schema.field import Field
from cybertools.composer.schema.interfaces import ISchemaFactory
from cybertools.composer.schema.schema import Schema


class SchemaFactory(object):
    """ Creates a cybertools.composer schema from an
        interface (a zope.schema schema).
    """

    implements(ISchemaFactory)
    adapts(Interface)

    fieldMapping = {
            schema.TextLine: ('textline',),
            schema.ASCIILine: ('textline',),
            schema.Password: ('password',),
            schema.Text: ('textarea',),
            schema.ASCII: ('textarea',),
            schema.Date: ('date',),
            schema.Datetime: ('date',),
            schema.Int: ('number',),
            schema.Bool: ('checkbox',),
            schema.Choice: ('dropdown',),
            schema.Bytes: ('fileupload',),
    }

    def __init__(self, context):
        self.context = context

    def __call__(self, interface, **kw):
        fieldMapping = self.fieldMapping
        fields = []
        for fname in schema.getFieldNamesInOrder(interface):
            field = interface[fname]
            if field.__class__ in fieldMapping:
                info = fieldMapping[field.__class__]
                voc = (getattr(field, 'vocabulary', ()) or
                       getattr(field, 'vocabularyName', None))
                f = Field(field.getName(),
                        fieldType=info[0],
                        required=field.required,
                        default=field.default,
                        default_method=getattr(field, 'default_method', None),
                        vocabulary=voc,
                        title=field.title,
                        description=field.description,
                        readonly=field.readonly,
                        nostore=getattr(field, 'nostore', False),)
                fields.append(f)
        return Schema(name=interface.__name__, *fields, **kw)
