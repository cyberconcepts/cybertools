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

#reactor.callLater(10, stopReactor)
#reactor.listenTCP(5222, EchoServerFactory())

def startup(event=None):
    printTime()
    d = globals()
    #d['event'] = event
    if hasZope and event is not None:
        conn =event.database.open()
        root = conn.root()[ZopePublication.root_name]
    d.update(locals())
    reactor.listenTCP(5001, getManholeFactory(d, admin='aaa'))

if __name__ == '__main__':
    startup()