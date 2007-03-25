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
login, logout and similar stuff.

$Id$
"""

import urllib
from zope.app import zapi
from zope.app.authentication.session import SessionCredentialsPlugin
from zope.app.component import hooks
from zope.app.i18n import ZopeMessageFactory as _
from zope.app.security.browser.auth import LoginLogout as BaseLoginLogout
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zope.app.security.interfaces import ILogoutSupported
from zope.cachedescriptors.property import Lazy
from zope.i18n import translate
from zope.publisher.interfaces.http import IHTTPRequest


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
        url = '%s/@@%s?%s' % (zapi.absoluteURL(site, request),
                              self.loginpagename,
                              urllib.urlencode({'camefrom': camefrom}))
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
                zapi.absoluteURL(self.context, self.request),
                translate(_('[Logout]'), context=self.request,
                          default='[Logout]'))
        else:
            return None


