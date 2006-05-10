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
Interfaces for a simple contact management framework to be used
as an example for some of the cybertools packages.

$Id$
"""

from zope.interface import Interface, Attribute
from zope import schema

class IPerson(Interface):
    """ Resembles a human being with a name (first and last name),
        a birth date, and a set of addresses.
    """

    firstName = schema.TextLine(title=u'The first name')
    lastName = schema.TextLine(title=u'The last name or surname')
    birthDate = schema.Date(title=u'The date of birth - '
                    'should be a datetime.date object')

    addresses = Attribute('A mapping whose values provide the IAddress '
                    'interface')

    age = Attribute('The current age in full years, so this should '
                    'be an integer calculated dynamically, i.e. a read-only '
                    'attribute')
