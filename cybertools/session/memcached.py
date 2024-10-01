# cybertools.session.memcached

""" Store session data in memcached.
"""

from zope.app.session.interfaces import IClientId, ISession
from zope.app.session.interfaces import ISessionDataContainer
from zope.app.session.interfaces import ISessionPkgData, ISessionData
from zope import component
from zope.component import getUtility, adapts
from zope.component.interfaces import ComponentLookupError
from zope.interface import implementer
from zope.publisher.interfaces import IRequest
from lovely.memcached.interfaces import IMemcachedClient


@implementer(ISessionDataContainer)
class SessionDataContainer(object):

    lifetime = 24 * 3600
    namespace = 'cybertools.session'

    def __getitem__(self, key):
        client = component.getUtility(IMemcachedClient)
        value = client.query(key, ns=self.namespace)
        if value:
            value.parent = self
        return value

    def __setitem__(self, key, value):
        client = component.getUtility(IMemcachedClient)
        oldValue = client.query(key, ns=self.namespace)
        if oldValue:
            oldValue.update(value)
            newValue = oldValue
        else:
            newValue = value
        client.set(newValue, key, lifetime=self.lifetime, ns=self.namespace)


@implementer(ISession)
class Session(object):

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


@implementer(ISessionData)
class SessionData(dict):

    def __init__(self, id, parent):
        self.id = id
        self.parent = parent

    def __getitem__(self, key):
        value = super(SessionData, self).__getitem__(key)
        if isinstance(value, SessionPkgData):
            value.parent = self
        return value

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


@implementer(ISessionPkgData)
class SessionPkgData(SessionData):

    def __getitem__(self, key):
        return super(SessionPkgData, self).__getitem__(key)
