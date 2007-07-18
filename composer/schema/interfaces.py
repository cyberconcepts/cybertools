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
Schemas and Fields.

$Id$
"""

from zope import schema
from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory

from cybertools.composer.interfaces import ITemplate, IComponent

_ = MessageFactory('zope')


class ISchema(ITemplate):
    """ Represents an ordered sequence of fields.
    """

    fields = Attribute('The components the schema is built up of. '
                'Should be a sequence of IField objects.')


class IField(IComponent):
    """ May be used for data entry or display.
    """

    name = schema.ASCII(
                    title=_(u'Fieldname'),
                    description=_(u'The internal name of the field'),
                    required=True,)
    title = schema.TextLine(
                    title=_(u'Title'),
                    description=_(u'The title or label of the field'),
                    required=True,)
    description = schema.Text(
                    title=_(u'Description'),
                    description=_(u'A more lengthy description of the field'),
                    required=False,)
    fieldType = schema.Choice(
                    title=_(u'Field type'),
                    description=_(u'The type of the field'),
                    required=True,
                    default='textline',
                    values=('textline', 'textarea', 'date'))
    defaultValue = schema.TextLine(
                    title=_(u'Default'),
                    description=_(u'Value with which to pre-set the field contents'),
                    required=False,)
    required = schema.Bool(
                    title=_(u'Required'),
                    description=_(u'Must a value been entered into this field?'),
                    required=False,)

