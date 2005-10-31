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
Implementation of classes providing lazy variables.

$Id$
"""

from zope.interface import implements
import interfaces

class LazyNamespace(object):
    """ Basic adapter providing a lazy namespace.
    """

    implements(interfaces.ILazyNamespace)

    variables = {}

    def __init__(self, context):
        self.context = context

    @classmethod
    def registerVariable(class_, name, method):
        class_.variables[name] = method

    def __getattr__(self, attr):
        value = self.variables[attr](self)
        setattr(self, attr, value)
        return value

    
class LazyBrowserNamespace(LazyNamespace):
    """ A multi-adapter providing a lazy namespace for to be used for
        browser views.
    """

    variables = {}  # LazyBrowserNamespace class should get its own registry.

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

        
    