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
Abstract base classes for type management.

$Id$
"""

from zope.interface import implements
from cybertools.typology.interfaces import IType, ITypeManager


class BaseType(object):

    implements(IType)

    def __init__(self, context):
        self.context = context

    def __eq__(self, other):
        return self.token == other.token

    title = u'BaseType'

    @property
    def token(self):
        return str(self.title.lower().replace(' ', '_'))

    @property
    def tokenForSearch(self): return self.token

    interfaceToProvide = None
    factory = None
    defaultContainer = None
    typeProvider = None


class TypeManager(object):

    implements(ITypeManager)

    @property
    def types(self):
        return (BaseType(None),)

    def listTypes(self, **criteria):
        return self.types

    def getType(self, token):
        for t in self.types:
            if t.token == token:
                return t
        raise ValueError('Unrecognized token: ' + token)

