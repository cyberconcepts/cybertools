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
Interfaces for import/export functionalities.

$Id$
"""

from zope.interface import Attribute, Interface


class IImporter(Interface):
    """ Parses an input file or string and creates one or more corresponding
        objects or sets the attributes of one or more existing objects.
    """

    transcript = Attribute('A string describing the result of the '
                    'import process.')
    changes = Attribute('A sequence of mappings describing the '
                    'objects that were created or modified by the '
                    'import process, together with information about '
                    'the changes.')
    errors = Attribute('A sequence of mappings describing the errors '
                    'during loading and the corresponding objects.')
    summary = Attribute('A simple mapping giving an overview of the numbers '
                    'of newly created and changed objects and the '
                    'number of errors.')

    def load(file):
        """ Load (import) data from the file given; create objects if
            necessary.
        """
