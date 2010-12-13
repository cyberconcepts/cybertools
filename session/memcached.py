#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
Store session data in memcached.

$Id$
"""

from zope.app.session.interfaces import IClientId, ISession
from zope.app.session.interfaces import ISessionDataContainer
from zope.app.session.interfaces import ISessionPkgData, ISessionData
from zope import component
from zope.component import getUtility, adapts
from zope.component.interfaces import ComponentLookupError
from zope.interface import implements
from zope.publisher.interfaces import IRequest
from lovely.memcached.interfaces import IMemcachedClient


class SessionDataContainer(object):

    implements(ISessionDataContainer)

    lifetime = 24 * 3600
    namespace = 'cybertools.session'

    def __getitem__(self, key):
        client = component.getUtility(IMemcachedClient)
        return client.query(key, ns=self.namespace)

    def __setitem__(self, key, value):
        client = component.getUtility(IMemcachedClient)
        #print '***', key, value
        client.set(value, key, lifetime=self.lifetime, ns=self.namespace)


class Session(object):

    implements(ISession)
    adapts(IRequest)

    packageName = 'cybertools.session.memcached'

    def __init__(self, request):
        self.client_id = str(IClientId(request))

    def __getitem__(self, pkg_id):
        sdc = getUtility(ISessionDataContainer, name=self.packageName)
        sd = sdc[self.client_id]
        if sd is None:
            sd = sdc[self.client_id] = SessionData(self.client_id, sdc)
        try:
            return sd[pkg_id]
        except KeyError:
            spd = sd[pkg_id] = SessionPkgData(pkg_id, sd)
            return spd


class SessionData(dict):

    implements(ISessionData)

    def __init__(self, id, parent):
        self.id = id
        self.parent = parent

    def __setitem__(self, key, value):
        super(SessionData, self).__setitem__(key, value)
        self.parent[self.id] = self

    def setdefault(self, key, default):
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

    def clear(self):
        super(SessionData, self).clear()
        self.parent[self.id] = self


class SessionPkgData(SessionData):

    implements(ISessionPkgData)

