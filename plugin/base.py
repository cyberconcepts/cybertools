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
Basic plug-in functionality.

$Id$
"""

from cybertools.plugin.manage import checkReload, registerFunction


def register(*ifc):

    def _register(fct):

        def _fct(*args, **kw):
            fctNew = checkReloadFunction(fct)
            if fctNew is None:
                raise ValueError('Function no longer present: %s.%s' %
                                    fct.__module__, fct.__name__)
            return fctNew(*args, **kw)

        registerFunction(_fct, fct, ifc)
        return _fct

    return _register


def checkReloadFunction(f):
    m = checkReload(f.__module__)
    if m:
        return getattr(m, f.__name__, None)
    return f
