# cybertools.composer.rule.web

""" Action handler for sending emails.
"""

from zope import component

from cybertools.composer.rule.interfaces import IRuleManager, IRuleInstance
from cybertools.composer.rule.interfaces import IActionHandler
from cybertools.composer.rule.base import ActionHandler
from cybertools.composer.schema.browser.common import BaseView
from cybertools.organize.service import getCheckoutRule


class RedirectActionHandler(ActionHandler):

    def __call__(self, data, params={}):
        request = data['request']
        targetView = params['viewName']
        messageName = params['messageName']
        if hasattr(request, 'URL1'):  # Zope 2 request
            url = request.URL1
        else:
            url = request.URL[-1]
        request.response.redirect('%s/%s?message=%s&ccln=yes'
                    % (url, targetView, messageName))
        return data


class MessageView(BaseView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getMessage(self):
        messageName = self.request.get('message')
        if not messageName:
            return '<h1>No message name given</h1>'
        rule = getCheckoutRule('dummy')  # the only rule existing atm
        clientName = self.getClientName()
        if not clientName:
            return '<h1>No client info found</h1>'
        client = self.context.getClients().get(clientName)
        ri = IRuleInstance(client)
        ri.template = rule
        data = dict(request=self.request)
        mh = component.getAdapter(ri, IActionHandler, name='message')
        data = mh(data, dict(messageName=messageName))
        if self.request.get('ccln'):
            self.setClientName('')
        return data['text']

