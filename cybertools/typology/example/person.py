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
cybertools.organize package

$Id$
"""

from zope.component import adapts
from zope.interface import implements
from cybertools.organize.interfaces import IPerson
from cybertools.typology.interfaces import IType, ITypeManager
from cybertools.typology.type import BaseType, TypeManager


# interfaces

class IAgeGroup(IType):
    """ A type interface for discerning childs and adults.
    """


class IAgeGroupManager(ITypeManager):
    """ A type manager managing age groups.
    """


# implementations

class AgeGroup(BaseType):

    implements(IAgeGroup)
    adapts(IPerson)

    # IType attributes

    @property
    def title(self):
        return self.isChild and u'Child' or u'Adult'

    @property
    def token(self): return 'organize.person.agegroup.' + str(self.title.lower())

    # helpers

    @property
    def isChild(self):
        return self.context.age < 18.0


class AgeGroupTypeInfo(AgeGroup):
    """ Age group type info object with fixed (not computed) isChild property.
    """

    isChild = None

    def __init__(self, isChild):
        self.isChild = isChild


class AgeGroupManager(TypeManager):

    implements(IAgeGroupManager)

    @property
    def types(self):
        return tuple([AgeGroupTypeInfo(flag) for flag in (True, False)])

