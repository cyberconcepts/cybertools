# cybertools.xedit.browser

""" (View) class(es) for the external editor functionality.
"""

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL


class ExternalEditorView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    # TODO: don't access context.data directly but via an IReadFile adapter

    def load(self, url=None):
        context = removeSecurityProxy(self.context)
        data = context.data
        r = []
        r.append('url:' + (url or absoluteURL(context, self.request)))
        r.append('content_type:' + str(context.contentType))
        r.append('meta_type:' + '.'.join((context.__module__,
                                          context.__class__.__name__)))
        r.append('title:' + fromUnicode(context.title))
        auth = self.request.get('_auth')
        if auth:
            print('ExternalEditorView: auth = ', auth)
            if auth.endswith('\n'):
                auth = auth[:-1]
            r.append('auth:' + auth)
        cookie = self.request.get('HTTP_COOKIE','')
        if cookie:
            r.append('cookie:' + cookie)
        r.append('')
        r.append(fromUnicode(data))
        r = [str(item) for item in r]
        result = '\n'.join(r)
        self.setHeaders(len(result))
        return result
        #return fromUnicode(result)

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
        response.setHeader('Content-Type', 'application/x-zope-edit')
        #response.setHeader('Content-Type', 'application/x-zope-xedit')
        response.setHeader('Content-Length', size)


def fromUnicode(text):
    if not text:
        return b''
    if isinstance(text, str):
        return text.encode('UTF-8')
    return text
