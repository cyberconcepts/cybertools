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
Action handler for sending emails.

$Id$
"""

from zope import component
from zope.interface import implements

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

