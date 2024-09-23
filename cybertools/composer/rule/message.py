# cybertools.composer.rule.message

""" Action handler for providing messages.
"""

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
        mi = MessageInstance(client, message, manager)
        #mi.template = message
        return mi.applyTemplate(data)
