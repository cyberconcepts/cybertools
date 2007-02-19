#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
(View) class(es) for the external editor functionality.

$Id$
"""

from zope.app import zapi
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.security.proxy import removeSecurityProxy


class ExternalEditorView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    # TODO: don't access context.data directly but via an IReadFile adapter

    def load(self, url=None):
        context = removeSecurityProxy(self.context)
        data = context.data
        r = []
        r.append('url:' + (url or zapi.absoluteURL(context, self.request)))
        r.append('content_type:' + str(context.contentType))
        r.append('meta_type:' + '.'.join((context.__module__, context.__class__.__name__)))
        auth = self.request.get('_auth')
        if auth:
            print 'ExternalEditorView: auth = ', auth
            if auth.endswith('\n'):
                auth = auth[:-1]
            r.append('auth:' + auth)
        cookie = self.request.get('HTTP_COOKIE','')
        if cookie:
            r.append('cookie:' + cookie)
        r.append('')
        r.append(data)
        result = '\n'.join(r)
        self.setHeaders(len(result))
        return fromUnicode(result)

    def save(self):
        data = self.request.get('editor.data')
        if data:
            self.context.data = data
            notify(ObjectModifiedEvent)

    def lock(self):
        pass

    def unlock(self):
        pass

    def setHeaders(self, size):
        response = self.request.response
        response.setHeader('Content-Type', 'application/x-zope-xedit')
        response.setHeader('Content-Length', size)


def fromUnicode(text):
    if not text:
        return ''
    if isinstance(text, unicode):
        return text.encode('UTF-8')
    return text
