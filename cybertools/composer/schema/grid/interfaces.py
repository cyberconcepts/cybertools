# cybertools.composer.schema.grid.interfaces

""" Grid field definition.
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

