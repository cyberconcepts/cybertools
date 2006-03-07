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
interface definitions for the typology package.

$Id$
"""

from zope.app.container.interfaces import IContainer
from zope import schema
from zope.configuration.fields import GlobalObject
from zope.interface import Interface, Attribute


class IType(Interface):
    """ Associated with an object (typically as an adapter) giving
        information about the object's type.
    """

    title = schema.TextLine(title=u'Title',
                description=u'A readable representation',
                required=True)
    token = schema.ASCIILine(title=u'Token',
                description=u'A representation used for identifying a type '
                              'temporarily, e.g. on forms',
                required=True)
    tokenForSearch = schema.ASCIILine(title=u'Token for Search',
                description=u'A fairly unique token that may be used '
                             'e.g. for identifying types via a catalog index')
    interfaceToProvide = GlobalObject(title=u'Interface to Provide',
                description=u'An (optional) interface that objects of this '
                             'type will provide')
    factory = GlobalObject(title=u'Factory',
                description=u'A factory (or class) that may be used for '
                             'creating an object of this type')
    defaultContainer = schema.Object(IContainer,
                title=u'Default Container',
                description=u'Where objects of this type will be created in '
                             'when no explicit container is given')
    typeProvider = schema.Object(Interface,
                title=u'Type Provider',
                description=u'A usually long-living object that corresponds '
                             'to the type. Note that this object need not '
                             'provide the IType interface itself')


class ITypeManager(Interface):
    """ A utility or utility-like object (e.g. a container) that may
        manage (store, retrieve, assign) types.
    """
