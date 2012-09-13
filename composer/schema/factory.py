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
Schema factory stuff.
"""

from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope import schema

from cybertools.composer.schema.field import Field
from cybertools.composer.schema.interfaces import ISchemaFactory
from cybertools.composer.schema.schema import Schema


class Email(schema.TextLine):

    __typeInfo__ = ('email',)


# put field type name and other info in standard field classes.
schema.Field.__typeInfo__ = ('textline',)
schema.Password.__typeInfo__ = ('password',)
schema.Int.__typeInfo__ = ('number',)
schema.Float.__typeInfo__ = ('decimal',)
schema.Choice.__typeInfo__ = ('dropdown',)


class SchemaFactory(object):
    """ Creates a cybertools.composer schema from an
        interface (a zope.schema schema).
    """

    implements(ISchemaFactory)
    adapts(Interface)

    fieldMapping = {
            #schema.TextLine: ('textline',),
            #schema.ASCIILine: ('textline',),
            #schema.Password: ('password',),
            schema.Text: ('textarea',),
            schema.ASCII: ('textarea',),
            schema.Date: ('date',),
            schema.Datetime: ('date',),
            #schema.Int: ('number',),
            #schema.Float: ('decimal',),
            schema.Bool: ('checkbox',),
            schema.List: ('list',),
            #schema.Choice: ('dropdown',),
            schema.Bytes: ('fileupload',),
            #Email: ('email',),
    }

    def __init__(self, context):
        self.context = context

    def __call__(self, interface, **kw):
        fieldMapping = self.fieldMapping
        fields = []
        omit = kw.pop('omit', [])
        include = kw.pop('include', [])
        for fname in schema.getFieldNamesInOrder(interface):
            if fname in omit:
                continue
            if include and fname not in include:
                continue
            field = interface[fname]
            info = fieldMapping.get(field.__class__)
            f = createField(field, info)
            fields.append(f)
        return Schema(name=interface.__name__, *fields, **kw)


def createField(field, info=None):
    if info is None:
        info = getattr(field, '__typeInfo__', ('textline',))
    voc = (getattr(field, 'vocabulary', ()) or
           getattr(field, 'vocabularyName', None))
    f = Field(field.getName(),
              fieldType=info[0],
              fieldTypeInfo=len(info) > 1 and info[1] or None,
              required=field.required,
              default=field.default,
              default_method=getattr(field, 'default_method', None),
              vocabulary=voc,
              title=field.title,
              description=field.description,
              readonly=field.readonly,
              #value_type=getattr(field, 'value_type', None),
              nostore=getattr(field, 'nostore', False),
              showEmpty=getattr(field, 'showEmpty', False),
              multiple=getattr(field, 'multiple', False),
              display_format=getattr(field, 'displayFormat', None),
              baseField=field,)
    return f
