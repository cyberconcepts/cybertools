"""
A simple twisted manhole that allows you to access a running Zope 3
instance via a python command line without having to run ZEO.

You may run it for testing purposes via `python manhole.py` (note that
the twisted library must be reachable via your PYTHONPATH) and log in
from another console window using `ssh -p 5001 admin@localhost`. The
password is defined below in the "reactor.listenTCP()" statement. The
manhole script may be stopped with Ctrl-C.

Note that this will open up a serious security hole on your computer
as now anybody knowing this password may login to the Python console
and get full access to the system with the permissions of the user
running the manhole script.

In order to use it with Zope copy the cybertools.twisted-configure.zcml
to the etc/package-includes directory of your Zope instance and restart
Zope. Open the manhole via the "Manhole Control" Tab of the "Manage process"
menu.

You can then log in with ssh like shown above, using the username
and password of the zope.manager principal defined in your principals.zcml.

After logging in use the `help` command to get more information.

$Id$
"""

from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic
from twisted.cred import portal, checkers, credentials, error as credError
from twisted.conch import manhole as manhole, manhole_ssh
from zope.interface import implements
try:
    from zope.app.publication.zopepublication import ZopePublication
    from zope.app.component.hooks import setSite
    from zope.app.security.principalregistry import principalRegistry
    from zope.app.security import settings
    from zope.app.security.interfaces import IAuthentication
    from zope.app.securitypolicy.principalrole import principalRoleManager
    from zope.app import zapi
    import transaction
    hasZope = True
except:
    hasZope = False
import time
import sys
from cStringIO import StringIO

listener = None
factory = None
printLog = None
port = 5001


def getManholeFactory(namespace, **passwords):
    realm = manhole_ssh.TerminalRealm()
    def getManhole(_):
        #return manhole.ColoredManhole(namespace)
        return manhole.Manhole(namespace)
    realm.chainedProtocolFactory.protocolFactory = getManhole
    p = portal.Portal(realm)
    checker = (hasZope and ZopeManagerChecker() or
                checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    p.registerChecker(checker)
    return manhole_ssh.ConchFactory(p)


class ZopeManagerChecker(object):

    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def requestAvatarId(self, credentials):
        login = credentials.username
        password = credentials.password
        # TODO: This should be based on the official Zope API stuff, e.g. via:
        #principalRegistry = zapi.getUtility(IAuthentication)
        principal = principalRegistry.getPrincipalByLogin(login)
        if principal.validate(password):
            roles = principalRoleManager.getRolesForPrincipal(principal.id)
            for role, setting in roles:
                if role == 'zope.Manager' and setting == settings.Allow:
                    return defer.succeed(login)
            return defer.fail(credError.UnauthorizedLogin(
                        'Insufficient permissions'))
        return defer.fail(credError.UnauthorizedLogin(
                    'User/password not correct'))


def printTime():
    global printLog
    print '***', time.strftime('%H:%M:%S'), '- twisted.manhole open ***'
    printLog = reactor.callLater(600, printTime)


class Help(object):
    
    def __repr__(self):
        info = """
        Use `dir()`  to see what variables and functions are available.
        """
        zopeInfo = """
        You may use `x = zapi.traverse(root, 'path/to/object')`  to get an
        object in your folder hierarchy. Then you may call any method or
        access any attribute of this object.
        
        In order to get access to local utilities and adapters you may
        issue a `setSite(root)`. Don't forget to call `setSite()` before
        finishing your session in order to reset this setting.

        If you change an object stored in the ZODB you should issue a
        `transaction.commit()` to make your changes permanent or a
        `transaction.abort()` to undo them.
        """
        return info + (hasZope and zopeInfo or '')

    def __call__(self):
        print self

help = Help()


def open(port=5001, request=None):
    global hasZope, factory, listener
    printTime()
    d = globals()
    if hasZope and request is not None:
        database = request.publication.db
        connection = database.open()
        root = connection.root()[ZopePublication.root_name]
    else:
        hasZope = False
    d.update(locals())
    namespace = {}
    for key in ('__builtins__', 'connection', 'event', 'setSite', 'hasZope',
                'zapi', 'transaction', 'root', '__doc__', 'help',
                'manholeFactory', 'context'):
        if key in d:
            namespace[key] = d[key]
    # TODO: get admin password from somewhere else or use a real checker.
    factory = getManholeFactory(namespace, admin='aaa')
    listener = reactor.listenTCP(port, factory)

def close():
    global listener
    listener.stopListening()
    listener = None


if __name__ == '__main__':
    port = 5001
    if len(sys.argv) > 1:
        port = int(sys.argv[-1])
    startup(port=port)
    reactor.run()

