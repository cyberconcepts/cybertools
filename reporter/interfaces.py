#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
interface definitions for the reporter package.

$Id$
"""

import zope
from zope.interface import Interface, Attribute


# iterable stuff for batching, sorting, filtering of results


class IBatch(Interface):
    """ Represents a part (sort of a slice) of an iterable.
    """

    iterable = Attribute(u'The iterable this batch belongs to')

    start = Attribute(u'The current start index of the batch in the parent iterable')
    
    def __getitem__(idx):
        """ Return the item at index idx.
        """

    def next():
        """ Return the next item in the batch. Raise StopIteration if
            the end of the batch is reached.
        """

    def __len__():
        """ Return the number of items in the batch.
        """

    def getIndexRelative(relativePageNumber):
        """ Return the absolute page index based on the current page of
            the batch object.
            Using +1 or -1 retrieves the next or previous batch.
            If a page before the first one is addressed return 0,
            if a page after the last one is addressed return the index
            of the last page.
        """

    def getIndexAbsolute(pageNumber):
        """ Return the absolute page index.
            0 addresses the first batch page, -1 the last.
            Return None if the corresponding page does not exist.
        """


# result sets, rows, cells...

class IResultSet(Interface):
    """A sequence of rows provided by a data source, report or
        similar object, together with a schema that describes the columns
        (fields, cells).
    """

    schema = zope.schema.Iterable(title=u'Schema',
                    description=u'Collection of field specifications based '
                                 'on the interfaces defined by zope.schema.')
    rows = zope.schema.Iterable(title=u'Rows',
                    description=u'Sequence of row objects')


class IRow(Interface):
    """ A sequence of cells containing the real data objects.
    """

    cells = zope.schema.Dict(zope.schema.ASCIILine(),
                    title=u'Cells',
                    description=u'Mapping of data elements addressed by a name '
                                 'that is the key to the mapping.')

    resultSet = Attribute('The result set this row belongs to.')


class ICell(Interface):
    """ A single cell of a listing or table.
    """

    text = zope.schema.Text(title=u'Text',
                    description=u'Text to be displayed')
    value = zope.schema.Object(Interface,
                    title=u'Value',
                    description=u'The real object, often identical to text.')
    token = zope.schema.ASCIILine(title=u'Token',
                    description=u'May be used to identify a cell within'
                                 'the result set, e.g. in forms')

    row = Attribute('The row this cell belongs to.')

    def sortKey():
        """ Returns a value (typically a string or a sequence) that will
            be used for comparing cells in order to sort rows.
        """


# data source

class IDataSource(Interface):
    """ An iterable that may be used as a data source.
    """

    def __iter__():
        """ Return an iterable that provides the data to be evaluated.
        """

