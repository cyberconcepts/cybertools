#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
Complex structures with templates/schemas.

$Id$
"""

from zope.interface import Interface, Attribute


# template side interfaces

class IComponent(Interface):
    """ Basic building block. A component may be part of other components.
    """


class IElement(IComponent):
    """ A final or elementary component, i.e. one that does not consist
        of other components.
    """


class ICompound(IComponent):
    """ A component that consists of other components.
    """

    parts = Attribute('An ordered sequence of the components this '
                      'object consists of')


class ITemplate(Interface):
    """ A structure, consisting of components, that may be used as a
        template/schema/blueprint for client objects.
    """

    components = Attribute('An ordered sequence of the components this '
                      'object is built upon')


# client side interfaces

class IInstance(Interface):
    """ Represents an object that uses a template.
    """

    parent = Attribute('The client this instance belongs to')
    template = Attribute('Template this instance is associated with')

    def applyTemplate(*args, **kw):
        """ Apply the template (in the parent's context). Note that this
            method is just an example - instance classes may define
            other methods that provide more specific actions.
        """


class IClient(Interface):
    """ Represents an object that uses a set of templates via its instances.
    """

    context = Attribute('Object this client adapter has been created for')
    instances = Attribute('An ordered or unordered sequence of instance objects')

    def applyTemplates(*args, **kw):
        """ Apply the templates of all instances. Note that this
            method is just an example - client classes may define
            other methods that provide more specific actions.
        """

