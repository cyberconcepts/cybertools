#
#  Copyright (c) 2005 Helmut Merz helmutm@cy55.de
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
interface definitions for the Relations utility and relation objects.

$Id$
"""

from zope.interface import Interface, Attribute


class IRelationsRepository(Interface):
    """ Local utility for storing relations.
    """

    def add(relation):
        """ Add the relation given and return the id generated for it.
        """

    def remove(relation):
        """ Remove the relation given.
        """
        

class IRelationsRegistry(Interface):
    """ Local utility for registering (cataloguing) and searching relations.
    """

    def register(relation):
        """ Register the relation given with this registry.
        """

    def unregister(relation):
        """ Remove the relation given from this registry.
        """

    def query(**kw):
        """ Return a list of relations that fulfill the criteria given.

            Example: rr.queryRelations(first=someObject, second=anotherObject,
                                       relationship='a.dotted.name')
        """


class IRelation(Interface):
    """ Base class for relations.
    """
    
    relationship = Attribute(
        'A string specific for a kind of relation; e.g. the full module '
        'path and class name of the class implementing a certain type of relation.')

    
class IDyadicRelation(IRelation):
    """ Relation connecting two objects.
    """

    first = Attribute('First object that belongs to the relation.')
    second = Attribute('Second object that belongs to the relation.')

    
class ITriadicRelation(IDyadicRelation):
    """ Relation connecting three objects.
    """
    
    third = Attribute('Third object that belongs to the relation.')

    