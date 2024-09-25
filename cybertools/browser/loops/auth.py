# cybertools.browser.loops.auth

""" login, logout and similar stuff.
"""

from urllib.parse import urlencode
from zope.app.security.browser.auth import LoginLogout as BaseLoginLogout
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.authentication.interfaces import ILogoutSupported
from zope.cachedescriptors.property import Lazy
from zope.component import hooks
from zope.i18n import translate
from zope.i18nmessageid import ZopeMessageFactory as _
from zope.pluggableauth.plugins.session import SessionCredentialsPlugin
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.browser import absoluteURL


class LoopsSessionCredentialsPlugin(SessionCredentialsPlugin):

    def challenge(self, request):
        if not IHTTPRequest.providedBy(request):
            return False
        site = hooks.getSite()
        #camefrom = request.getURL() # wrong when object is not viewable
        #camefrom = request.getApplicationURL() + request['PATH_INFO']
        path = request['PATH_INFO'].split('/++/')[-1] # strip virtual host stuff
        if not path.startswith('/'):
            path = '/' + path
        camefrom = request.getApplicationURL() + path
        if 'login' in camefrom:
            camefrom = '/'.join(camefrom.split('/')[:-1])
        url = '%s/@@%s?%s' % (absoluteURL(site, request),
                              self.loginpagename,
                              urlencode({'camefrom': camefrom}))
        request.response.redirect(url)
        return True


class LoginLogout(BaseLoginLogout):

    def __call__(self):
        if IUnauthenticatedPrincipal.providedBy(self.request.principal):
            return u'<a href="@@login.html">%s</a>' % (
                #urllib.quote(self.request.getURL()),
                translate(_('[Login]'), context=self.request,
                          default='[Login]'))
        elif ILogoutSupported(self.request, None) is not None:
            return u'<a href="@@logout.html?nextURL=%s/login.html">%s</a>' % (
                absoluteURL(self.context, self.request),
                translate(_('[Logout]'), context=self.request,
                          default='[Logout]'))
        else:
            return None


