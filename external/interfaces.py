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



class IElement(Interface):
    """ A dicionary-like information element that is able to represent an
        object, a relation between objects or a special attribute.
        The attributes of the object are represented by items of
        the dictionary; the attribute values may be strings, unicode strings,
        or IElement objects.
    """

    elementType = Attribute('A string denoting the element type.')
    object = Attribute('The object that has been created from this '
                'element during import.')
    parent = Attribute('An optional parent element that this element is part of.')
    subElements = Attribute('An optional list of sub-elements; initially None.')

    def processExport(extractor):
        """ Will be called by the extractor during export to allow for
            special handling e.g. of certain attributes.
        """

    def add(element):
        """ Add a sub-element, may be called by the extractor during export.
        """

    def execute(loader):
        """ Create the object that is specified by the element in the
            context of the loader and return it.
        """


# import functionality

class IReader(Interface):
    """ Provides objects in an intermediate format from an external source.
        Will typically be implemented by an utility or an adapter.
    """

    def read(input):
        """ Retrieve content from the external source returning a sequence
            of IElement objects.
        """


class ILoader(Interface):
    """ Inserts data provided by an IReader object into the
        object space of the context object. Will typically be used as an adapter.
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

    def load(elements):
        """ Create the objects and relations specified by the ``elements``
            argument given.
        """


# export functionality

class IWriter(Interface):
    """ Transforms object information to an external storage.
    """

    def write(elements):
        """ Write the sequence of elements given in an external format.
        """


class IExtractor(Interface):
    """ Extracts information from objects and provides them as
        IElement objects. Will typically be used as an adapter on a
        top-level or root object.
    """

    count = Attribute('Number of elements extracted.')

    def extract():
        """ Creates and returns a sequence of IElement objects by scanning
            the content of the context object.
        """

class ISubExtractor(IExtractor):
    """ Used for extracting special informations from individual objects
        that will be represented by sub-elements.
    """
