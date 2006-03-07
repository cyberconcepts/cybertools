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
Example classes for the cybertools.reporter package. These use the
cybertools.contact package

$Id$
"""

# TODO: move generic stuff to type.Type class

from zope.component import adapts
from zope.interface import implements
from cybertools.contact.interfaces import IPerson
from cybertools.typology.interfaces import IType

class BasicAgeGroup(object):

    implements(IType)
    adapts(IPerson)

    def __init__(self, context):
        self.context = context

    def __eq__(self, other):
        return self.token == other.token

    # IType attributes

    @property
    def title(self):
        return self.isChild() and u'Child' or u'Adult'

    @property
    def token(self): return 'contact.person.agetype.' + str(self.title.lower())

    @property
    def tokenForSearch(self): return self.token

    # helper methods

    def isChild(self):
        return self.context.age < 18.0

