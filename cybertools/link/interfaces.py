#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
Interfaces for Wiki functionality.

$Id$
"""

from zope.interface import Interface, Attribute
from zope import schema


class ILinkManager(Interface):
    """ Manages (and possibly contains) all kinds of wiki-related links.
    """

    def createLink(name, source, target, **kw):
        """ Create, register, and return a link record.

            Optional attributes are given as keyword arguments.
        """

    def removeLink(link):
        """ Remove a link.
        """

    def getLink(identifier):
        """ Return the link record identfied by the identifier given or None if
            not present.
        """

    def query(name=None, source=None, target=None, **kw):
        """ Search for link records matching the criteria given. One of
            name, source or target must be given.
        """

    def __iter__():
        """ Return an iterator of all links.
        """


class ILink(Interface):
    """ A directed link (connection, relation) between two local or foreign
        objects.

        The combination of name and source usually uniquely identfy a link.
    """

    identifier = Attribute('An internal identifier of the link record, '
                'unique within the link manager.')
    name = Attribute('The external identifier for the link, i.e. the '
                'string used in the source text to address the link.')
    source = Attribute('Identifier of the link\'s source object.')
    target = Attribute('Identifier of the link\'s target object or - '
                'for external links - the target URI.')
    linkType = Attribute('Optional: A short string specifying the type of the '
                'link, a sort of predicate; default: "link".')
    title = Attribute('Optional: A short text, may be used as the default text for '
                'the link or for the alt tag of an image.')
    description = Attribute('Optional: some text, may be used as a title attribute.')
    state = Attribute('Optional: A short string denoting the state of the link '
                'entry; default: "valid"')
    relevance = Attribute('Optional: A float number between 0.0 and 1.0 denoting '
                'the relevance of the connection between source and target; '
                'default: 1.0.')
    order = Attribute('Optional: An integer that may be used when providing an '
                'ordered listing of links; default: 0.')
    targetFragment = Attribute('Optional: an address part leading to a '
                'text anchor or the part of an image.')
    targetParameters = Attribute('Optional: a dictionary of URI parameters '
                'that will have to be appended to the link to the target object.')
    creator = Attribute('Optional: a string denoting the creator of the record.')

    def getManager():
        """ Return the link manager this link is managed by.
        """
