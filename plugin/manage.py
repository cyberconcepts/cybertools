#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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
Plug-in management.

$Id$
"""

import os, sys, time
from zope import component


class PluginModule(object):

    def __init__(self, module):
        self.name = module.__name__
        self.module = module
        self.timeStamp = time.time()
        self.functions = dict()
        self.interfaces = dict()

    def registerFunction(self, f, name, ifc):
        self.functions[name] = f
        self.interfaces[name] = ifc


modules = dict()


def registerModule(m):
    pm = PluginModule(m)
    modules[m.__name__] = pm
    return pm


def registerFunction(wrapped, base, ifc):
    m = sys.modules[base.__module__]
    pm = modules.get(m.__name__)
    if pm:
        if base.__name__ in pm.functions:
            ifcOld = pm.interfaces[base.__name__]
            if ifcOld:
                gsm = component.getGlobalSiteManager()
                gsm.unregisterHandler(pm.functions[base.__name__], ifcOld)
    if pm is None or pm.module != m:
        pm = registerModule(m)
    pm.registerFunction(wrapped, base.__name__, ifc)
    if ifc:
        component.provideHandler(wrapped, ifc)


# automatic reloading

def checkReload(m):
    if isinstance(m, str):
        m = sys.modules[m]
    fpath, ext = os.path.splitext(os.path.abspath(m.__file__))
    src = fpath + '.py'
    pm = modules[m.__name__]
    mtime = pm.timeStamp
    if os.path.getmtime(src) > mtime:
        m = reload(m)
        pm.timeStamp = time.time()
        return m
    return False


def loadModules(*mods):
    for m in mods:
        checkReload(m)

