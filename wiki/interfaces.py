#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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


class IWikiManager(Interface):
    """ Manages wikis and wiki-related objects, like plugins.
    """

    wikis = Attribute('A collection of wikis managed by this object.')

    def addWiki(wiki):
        """ Register the wiki given.
        """

    def removeWiki(wiki):
        """ Remove the wiki given from the list of wikis.
        """


class IWiki(Interface):
    """ A collection of wiki pages, or - more generally - wiki components.
    """

    manager = Attribute('The wiki manager this wiki is managed by.')
    name = Attribute('The name or address of the wiki unique within the '
                'scope of the wiki manager.')
    pages = Attribute('A collection of the pages belonging to this wiki.')

    def createPage(name, title=None):
        """ Create a new wiki page identified by the name (address -
            may be a path) given and return it.
        """

    def removePage(name):
        """ Remove the page identified by name from the wiki, cleaning up
            all information related to the page.
        """


class IWikiPage(Interface):
    """ An object representing a page of a wiki.
    """

    wiki = Attribute('The wiki this page belongs to.')
    name = Attribute('A page name or address unique within the wiki.')
    title = Attribute('A short string describing the wiki page the may be '
                'use as a page title.')
    text = Attribute('The page content in input text format.')

    def render():
        """ Convert the text of the page to presentation format.
        """

    def parse():
        """ Convert the text of the page to a document tree.
        """

    def write(tree):
        """ Convert the document tree given to presentation format.
        """


# wiki elements

class ILinkManager(Interface):
    """Manages (and possibly contains) all kinds of wiki-related links.
    """

    def registerLink(link):
        """Register (store) a link.
        """

    def unregisterLink(link):
        """Remove a link.
        """


class ILink(Interface):
    """A hyperlink between two local or foreign objects.
    """

    identifier = Attribute('Identifier of the link, unique within its link manager.')
    manager = Attribute('The manager that this link is managed by.')
    formatName = Attribute('Name of the link format that identified the link.')

    source = Attribute('Link source.')
    target = Attribute('Link target.')


class IFormat(Interface):
    """Identifies links in texts and transforms text correspondingly.
    """

    manager = Attribute('The Wiki manager this format is associated with.')


class IFormatInstance(Interface):

    def unmarshall(text):
        """Analyse the text given extracting all links and registering them
        with the link manager; return text with all links transformed to
        an internal link naming format.

        This is typically used for preprocessing the text after editing.
        """

    def marshall(text):
        """Scan text for all links (i.e. substrings corresponding to the
        internal link naming format) and replace them with their external
        format.

        This is typically used for preparing a text for editing.
        """

    def display(text):
        """Scan text for all links (i.e. substrings corresponding to the
        internal link naming format) and replace them with their display
        format.

        The result will then be used for rendering by the text format.
        """
