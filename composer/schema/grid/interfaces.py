#
#  Copyright (c) 2013 Helmut Merz helmutm@cy55.de
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
Grid field definition.
"""

from zope import schema
from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from cybertools.composer.schema.interfaces import FieldType

_ = MessageFactory('cybertools.composer.schema')


class Grid(schema.List):

    __typeInfo__ = ('grid',
                    FieldType('grid', 'grid',
                              u'Grid for representing a series of records or rows.',
                              instanceName='grid'))

    column_types = []
    ignoreInCheckOnEmpty = []
    cardinality = None


class Records(Grid):

    __typeInfo__ = ('records',
                    FieldType('records', 'records',
                              u'A series of records or rows.',
                              displayRenderer='display_records',
                              instanceName='records',))


class RecordsTable(Grid):

    __typeInfo__ = ('recordstable',
                    FieldType('recordstable', 'recordstable',
                              u'A series of records or rows.',
                              displayRenderer='display_records',
                              inputRenderer='input_records',
                              instanceName='recordstable',))


class KeyTable(Grid):

    __typeInfo__ = ('keytable',
                    FieldType('keytable', 'keytable',
                              u'A dictionary of records or rows the first '
                              u'column of which represents the key.',
                              displayRenderer='display_records',
                              inputRenderer='input_records',
                              instanceName='keytable',))

