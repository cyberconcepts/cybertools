
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
Layouts and layout elements and their association with content objects.

$Id$
"""

from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from cybertools.composer.interfaces import ITemplate, IComponent
from cybertools.composer.interfaces import IInstance

_ = MessageFactory('cybertools.composer.layout')


class ILayoutManager(Interface):
    """ A utility that manages layouts and regions.
    """

    def getLayouts(regionName, instance):
        """ Return a sequence of layouts for the region given that are
            valid sub-layouts for the layout instance given.
        """

    def check(layout, instance):
        """ Return True if the layout given is a valid sub-layout
            for the instance given.
        """



class ILayout(ITemplate):
    """ Represents an ordered sequence of layout elements.
    """

    name = schema.ASCIILine(
                title=_(u'Layout Name'),
                description=_(u'The internal name of the layout.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title of the layout'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A medium-length description.'),
                required=False,)
    category = schema.ASCIILine(
                title=_(u'Layout category'),
                description=_(u'The name of a layout category this layout '
                    u'belongs to.'),
                required=False,)
    regionName = schema.ASCIILine(
                title=_(u'Region Name'),
                description=_(u'A dotted name that specifies the region '
                    u'this layout should be used for.'),
                required=True,)

    renderer = Attribute(u'An object responsible for rendering the layout.')
    order = Attribute(u'A number that may be used as a sorting key.')
    sublayouts = Attribute(u'A set of names explicitly specifying sub-layouts '
                    u'for this layout.')


class ILayoutComponent(IComponent):
    """ May be used for data entry or display.
    """

    name = schema.ASCIILine(
                title=_(u'Component name'),
                description=_(u'The internal name of the component.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title or label of the component.'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A medium-length description.'),
                required=False,)

    componentType = Attribute(u'The type of the component, e.g. an image, '
                    u'plain or HTML text, a reference to an object to be shown, '
                    u'or a listing, ...')


class ILayoutInstance(IInstance):
    """ An instance adapter for an arbitrary client object that associates
        it with a layout.
    """

    renderer = Attribute(u'An object responsible for rendering the layout.')

    def getLayouts(region):
        """ Return a sequence of sub-layouts for the region given.
        """


class IRegion(Interface):
    """ A part of a layout "canvas" that may be filled with layout objects.
    """

    name = schema.ASCIILine(
                title=_(u'Region name'),
                description=_(u'The internal name of the region.'),
                required=True,)
    allowedLayoutCategories = schema.List(
                title=_(u'Allowed layout categories'),
                description=_(u'A collection of names of layout categories '
                        u'to which layouts may belong that may be placed '
                        u'in this region.'),
                value_type=schema.ASCIILine(),
                required=False,)

    layouts = Attribute(u'The layouts currently assigned to this region.')
