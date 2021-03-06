#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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
from cybertools.composer.interfaces import IInstance

_ = MessageFactory('zope')


class IMessageManager(Interface):
    """ A manager (or container) for complex messages.
    """

    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title of the object.'),
                required=True,)

    messages = Attribute('A collection of message objects managed.')

    def addMessage(name, text):
        """ Add a message under the name given with the given message text.
        """


class IMessage(ITemplate):
    """ A complex message that may be expanded using instance data.
    """

    name = schema.ASCIILine(
                title=_(u'Name'),
                description=_(u'The internal name of the message.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title or label of the message.'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A brief description of the message.'),
                required=False,)
    subjectLine = schema.TextLine(
                title=_(u'Subject'),
                description=_(u'A short text that may be used as the subject '
                        'line for emails or as a page title for web pages.'),
                required=False,)
    text = schema.Text(
                title=_(u'Text'),
                description=_(u"The message text; may contain placeholders "
                        "i.e. words beginning with a '$' that will "
                        "be replaced when the message is rendered."),
                required=False,)
    format = schema.Choice(
                title=_(u'Text input format'),
                description=_(u'The format in which the message is entered.'),
                required=True,
                default='text/plain',
                values=('text/plain', 'text/html',))
    outputFormat = schema.Choice(
                title=_(u'Output format'),
                description=_(u'The format in which the message will be '
                        'rendered when delivered to the recipient.'),
                required=False,
                default='text/plain',
                values=('text/plain', 'text/html',))
    media = schema.Choice(
                title=_(u'Output media'),
                description=_(u'The media type on which the message will '
                        'be rendered.'),
                required=True,
                default='mail',
                values=('mail', 'browser',))

    manager = Attribute('The manager of this message object')

