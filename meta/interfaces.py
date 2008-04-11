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
Interfaces for the 'meta' package.

$Id$
"""

from zope.interface import Interface, Attribute


class IOptions(Interface):
    """ Provide a set of options (settings, configuration options,
        preferences) based on a given context object or loaded from
        a file.
    """

    def __contains__(key):
        """ Return True if this object provides the option identified
            by the key given.
        """

    def __iter__():
        """ Return an iterator over the option keys provided by this
            object.
        """

    def values():
        """ Return an iterator over all settings.
        """

    def __getitem__(key):
        """ Return the value belonging to the key given.
        """

    def __getattr__(key):
        """ Return the value belonging to the key given
            (same as ``__getitem__()``).
        """

    def __str__():
        """ Return a string representation that shows all settings.
        """


class IConfigurator(Interface):
    """ Adapter for an IOptions object that allows loading and saving
        of configuration settings.
    """

    def load(text=None, file=None):
        """ Load settings from the string or the file given.

            The ``file`` argument may be a string - that will be interpreted
            as a file name or path - or a file object
        """

    def dump(file=None):
        """ Return a string representation of the context's configuration
            settings; if ``file`` is given write the representation to
            the corresponding file object.
        """
