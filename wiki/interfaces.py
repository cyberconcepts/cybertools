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


# links

class ILinkManager(Interface):
    """Manages (and possibly contains) links of all kinds.
    """

    def register(link):
        """Register (store) a link.
        """

    def unregister(link):
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


class ILinkFormat(Interface):
    """Identifies links in texts and transforms text correspondingly.
    """

    manager = Attribute('The link manager this link format is associated with.')

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
