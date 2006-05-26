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
Interfaces for knowledge management and e-learning.

$Id$
"""

from zope.interface import Interface, Attribute
from zope import schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zope')


class IKnowledgeElement(Interface):
    """ An entity denoting some sort of knowledge.
    """

    parent = Attribute('An optional parent element (sort of parent topic)')

    def getDependencies():
        """ Return a collection of knowledge elements this object depends on.
        """

    def dependsOn(element):
        """ Add an element to the collection of elements this object
            depends on.
        """

    def removeDependency(element):
        """ Remove the element given from the collection of elements
            this object depends on.
        """

    def getDependents():
        """ Return a collection of knowledge elements that are depending
            on this object.
        """

    def getKnowers():
        """ Return a collection of Knowing objects that have this object
            in their knowledge portfolio.
        """

    def getProviders():
        """ Return a collection of knowledge providers that provide this
            object. 
        """


class IKnowing(Interface):
    """ Someone who knows something.
    """

    def getKnowledge():
        """ Return the collection of elements that constitute the
            knowledge of this object.
        """

    def knows(self, element):
        """ Add an element to the collection of elementsthat constitute the
            knowledge of this object.
        """

    def removeKnowledge(element):
        """ Remove the element given from the collection of elements
            that constitute the knowledge of this object.
        """

    def getMissingKnowledge(position):
        """ Return a tuple of knowledge elements that this object
            is missing for fulfilling the position given.
        """

    def getProvidersNeeded(position):
        """ Return a tuple of tuples: Each tuple has as its first element
            a requirement of the position, the second element is a tuple
            of the knowledge providers providing this knowledge
            ((requirement, (provider, ...,)), ...).
        """


class IPosition(Interface):
    """ A position requires a certain knowledge.
    """

    def getRequirements():
        """ Return the collection of knowledge elements this object requires.
        """

    def requires(element):
        """ Add a knowledge element to the collection of elements this
            object requires.
        """

    def removeKnowledge(element):
        """ Remove the element given from the collection of elements
            this object requires.
        """


class IKnowledgeProvider(Interface):
    """ An object that is able to provide a certain knowledge - that may
        be a document or some sort of elearning content, ...
    """

    def getProvidedKnowledge():
        """ Return a collection of knowledge elements this object provides.
        """

    def provides(element):
        """ Add a knowledge element to the collection of elements this
            object provides.
        """

    def removeProvidedKnowledge(element):
        """ Remove the element given from the collection of elements
            this object provides.
        """



