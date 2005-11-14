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
from zope.app.event.interfaces import IObjectEvent


# relation interfaces

class IRelation(Interface):
    """ Base interface for relations.
    """
    
    def getPredicateName():
        """ Return the predicate of this relation as a string that may be
            used for indexing.
        """

    def validate(registry=None):
        """ Return True if this relation is valid.

            If the registry argument is provided the check should be done
            with respect to this relation registry, e.g. to 
        """


class IMonadicRelation(IRelation):
    """ Relation with just one object.

        While a monadic relation could be easily represented by an attribute
        or an annotation, monadic relations are e.g. useful when working with
        an ontology-driven higher-level relation framework.
    """

    first = Attribute('First and only object that belongs to the relation.')
        
    
class IDyadicRelation(IRelation):
    """ Relation connecting two objects.
    """

    first = Attribute('First object that belongs to the relation.')
    second = Attribute('Second object that belongs to the relation.')

    
class ITriadicRelation(IDyadicRelation):
    """ Relation connecting three objects.
    """
    
    third = Attribute('Third object that belongs to the relation.')


class IPredicate(Interface):
    """ A predicate signifies a relationship. This may be implemented
        directly as a relation class, or the relation object may 
        hold the predicate as an attribute.
    """
    
    def getPredicateName():
        """ Return this predicate as a string that may be used for indexing.
        """
        

# event interfaces

class IRelationInvalidatedEvent(IObjectEvent):
    """ This event fires when a relation is invalidated, typically because
        an object that is involved in the relation is removed.
    """


# relations registry interfaces
    
class IRelationsRegistryUpdate(Interface):
    """ Interface for registering and unregistering relations with a
        relations registry.
    """

    def register(relation):
        """ Register the relation given with this registry.
        """

    def unregister(relation):
        """ Remove the relation given from this registry.
        """


class IRelationsRegistryQuery(Interface):
    """ Interface for querying a relations registry.
    """

    def query(relation=None, **kw):
        """ Return a sequence of relations that fulfill the criteria given.

            You may provide a relation object as an example that specifies the
            search criteria, i.e. its predicate and first, second or third
            attribute will be used for searching, or explicit criteria
            via keyword arguments.
            
            Example for using keyword criteria:
                rr.queryRelations(first=someObject, second=anotherObject,
                                  relationship=SomeRelationClass)
        """


class IRelationsRegistry(IRelationsRegistryUpdate, IRelationsRegistryQuery):
    """ A registry for registering and searching relations typically
        implemented as a local utility .
    """

