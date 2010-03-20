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
Report management.

$Id$
"""

from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory
from zope import schema

from cybertools.composer.interfaces import ITemplate, IComponent
from cybertools.composer.interfaces import IInstance

_ = MessageFactory('cybertools.composer')


class IReportManager(Interface):
    """ A manager (or container) for complex messages.
    """

    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title of the object.'),
                required=True,)

    reports = Attribute('A collection of message objects managed.')

    def addReport(report):
        """ Add a report.
        """


class IReport(Interface):
    """ A complex message that may be expanded using instance data.
    """

    identifier = schema.ASCIILine(
                title=_(u'Identifier'),
                description=_(u'The (internal) identifier of the report.'),
                required=True,)
    name = schema.ASCIILine(
                title=_(u'Name'),
                description=_(u'The (visible) name of the report.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title or label of the report.'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A brief description of the report.'),
                required=False,)

    manager = Attribute('The manager of this message object')

