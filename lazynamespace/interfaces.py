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
interface definitions for the LazyVars stuff.

$Id$
"""

from zope.interface import Interface, Attribute


class ILazyNamespace(Interface):
    """ Generic adapter that provides lazy setting and returning
        of variables.
    """

    def registerVariable(class_, name, function):
        """ Class method: register a variable 'name' on class 'class_' that
            will be provided by calling the function given.

            The function should have one parameter that is set to the
            LazyNamespace object when the function is called. Thus the method
            has access to the instance variables (and other methods) of the
            LazyVars object.
        """

