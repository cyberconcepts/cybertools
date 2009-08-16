
"""
Code to be called at Zope startup.

$Id$
"""

from twisted.internet import reactor
from OFS.Application import AppInitializer
from zope.event import notify
from zope.app.appsetup.interfaces import DatabaseOpenedWithRoot


def startup(event):
    print '*** Database opened: %s' % event.database
    #twisted_target(event.database)


base_install_standards = AppInitializer.install_standards

def install_standards(self):
    result = base_install_standards(self)
    notify(DatabaseOpenedWithRoot(self.getApp()._p_jar.db()))
    return result

#AppInitializer.install_standards = install_standards
#print '*** AppInitializer monkey patch installed'


def twisted_target(db):
    reactor.callLater(5, show_application, db)


def show_application(db):
    c = db.open()
    print '*** Application: %s' % c.root()['Application']
    c.close()
    reactor.callLater(5, show_application, db)
