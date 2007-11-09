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
Action handler for providing messages.

$Id$
"""

from zope.interface import implements

from cybertools.composer.message.interfaces import IMessageManager
from cybertools.composer.message.instance import MessageInstance
from cybertools.composer.rule.base import ActionHandler


class MessageActionHandler(ActionHandler):

    def __call__(self, data, params={}):
        messageName = params.get('messageName')
        if messageName is None:
            raise ValueError('No message name given.')
        rule = self.context.template
        client = self.context.context
        manager = IMessageManager(client.manager)
        message = manager.messages.get(messageName)
        if message is None:
            raise ValueError('Message %s does not exist.' % messageName)
        #client = IClient(self.context)
        mi = MessageInstance(client, message)
        #mi.template = message
        return mi.applyTemplate(data)
