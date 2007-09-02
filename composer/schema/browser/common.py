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
Common base class(es) for schema and other template views.

$Id$
"""

from zope import component
from zope.app.session.interfaces import ISession
from zope.cachedescriptors.property import Lazy

from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.interfaces import IClientFactory


packageId = 'cybertools.composer.schema'


class BaseView(object):

    clientName = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getClientName(self):
        clientName = self.clientName
        if clientName:
            return clientName
        clientName = self.request.form.get('id')
        if clientName:
            self.setSessionInfo('clientName', clientName)
        else:
            clientName = self.getSessionInfo('clientName')
        self.clientName = clientName
        return clientName

    def setClientName(self, clientName):
        self.clientName = clientName
        self.setSessionInfo('clientName', clientName)

    def formatClientInfo(self, data, default=None):
        info = ' '.join((data.get('standard.firstName', ''),
                         data.get('standard.lastName', ''))).strip()
        org = data.get('standard.organization', '')
        info = ', '.join([text for text in (info, org) if text])
        return info or (default is None and data.get('__name__', '???')) or default

    @Lazy
    def manager(self):
        return self.context.getManager()

    @Lazy
    def previousTemplate(self):
        return self.getPreviousTemplate()

    def getPreviousTemplate(self):
        templates = self.context.getManager().getClientSchemas()
        context = self.context
        idx = templates.find(context)
        if idx > 0:
            #return templates[idx-1].name
            return templates.keys()[idx-1]
        else:
            return None

    @Lazy
    def nextTemplate(self):
        return self.getNextTemplate()

    def getNextTemplate(self):
        templates = self.context.getManager().getClientSchemas()
        context = self.context
        idx = templates.find(context)
        if 0 <= idx < len(templates) - 1:
            #return templates[idx+1].name
            return templates.keys()[idx+1]
        else:
            return None

    @Lazy
    def url(self):
        from zope.traversing.browser import absoluteURL
        return absoluteURL(self.context, self.request)

    buttonActions = dict(
            submit_previous=getPreviousTemplate,
            submit_next=getNextTemplate,
    )

    #@Lazy
    def nextUrl(self):
        #viewName = 'thankyou.html'
        viewName = ''
        form = self.request.form
        for bn in self.buttonActions:
            if bn in form:
                viewName = self.buttonActions[bn](self)
                break
        return '%s/%s?id=%s' % (self.url, viewName, self.clientName)

    def setSessionInfo(self, key, value, packageId=packageId):
        session = ISession(self.request)[packageId]
        if session.get(key) != value:
            session[key] = value

    def getSessionInfo(self, key, default=None, packageId=packageId):
        session = ISession(self.request)[packageId]
        return session.get(key, default)
