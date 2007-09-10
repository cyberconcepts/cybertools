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
Message management.

$Id$
"""

from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory
from zope import schema

from cybertools.composer.interfaces import ITemplate, IComponent

_ = MessageFactory('zope')


class IMessageManager(Interface):
    """ A manager (or container) for complex messages.
    """

    messages = Attribute('A collection of message objects managed.')


class IMessage(ITemplate):
    """ A complex message that may be expanded using instance data.
    """

    manager = Attribute('The manager of this message object')

    text = schema.Text()

