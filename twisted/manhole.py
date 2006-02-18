"""
$Id$
"""

from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.cred import portal, checkers
from twisted.conch import manhole, manhole_ssh
try:
    from zope.app.publication.zopepublication import ZopePublication
    from zope.app.component.hooks import setSite
    from zope.app import zapi
    hasZope = True
except:
    hasZope = False
import time
import sys
from cStringIO import StringIO

def getManholeFactory(namespace, **passwords):
    realm = manhole_ssh.TerminalRealm()
    def getManhole(_):
        return manhole.Manhole(namespace)
    realm.chainedProtocolFactory.protocolFactory = getManhole
    p = portal.Portal(realm)
    p.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    return manhole_ssh.ConchFactory(p)

def printTime():
    print 'twisted.manhole running:', time.strftime('%H:%M:%S')
    reactor.callLater(60, printTime)

def help():
    info = """
    Use  dir()  to see what variables and functions are available."""
    zopeInfo = """
    In order to get access to local utilities and adapters you should
    issue a  setSite(root). Don't forget to call  setSite()  before
    finishing your session.
    You may use  x = zapi.traverse(root, 'path/to/object')  to get an
    object in your folder hierarchy. Then you may call any method or
    access any attribute of this object."""
    print info
    if hasZope:
        print zopeInfo
    print


def startup(event=None, port=5001):
    global hasZope
    printTime()
    d = globals()
    if hasZope and event is not None:
        conn =event.database.open()
        root = conn.root()[ZopePublication.root_name]
    else:
        hasZope = False
    d.update(locals())
    namespace = {}
    for key in ('__builtins__', 'conn', 'event', 'setSite', 'hasZope', 'zapi',
                'root', '__doc__', 'help'):
        if key in d:
            namespace[key] = d[key]
    # TODO: get admin password from somewhere else or use a real checker.
    reactor.listenTCP(port, getManholeFactory(namespace, admin='aaa'))

if __name__ == '__main__':
    port = 5001
    if len(sys.argv) > 1:
        port = int(sys.argv[-1])
    startup(port=port)
    reactor.run()

