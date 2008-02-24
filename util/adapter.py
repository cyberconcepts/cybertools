#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
A simple adapter framework.

$Id$
"""


class AdapterFactory(object):

    def __init__(self):
        self._registry = {}

    def register(self, adapter, adapted, name=''):
        """ Register `adapter` class for objects of class `adapted`.
            Optionally associate the adapter with a `name`; thus there
            can be more than one adapter for one class.
        """
        self._registry[(adapted, name)] = adapter

    def queryAdapter(self, obj, name):
        class_ = type(obj) is type and obj or obj.__class__
        adapter = None
        while adapter is None and class_:
            adapter = self._registry.get((class_, name))
            if adapter is None:
                bases = class_.__bases__
                class_ = bases and bases[0] or None
        return adapter

    def __call__(self, obj, name=''):
        """ Return an adapter instance on `obj` with the `name` given.
            if obj is a class use this class for the adapter lookup, else
            use obj's class.
            If there isn't an adapter directly for the class
            check also for its base classes.
        """
        adapter = self.queryAdapter(obj, name)
        if adapter is None:
            return None
        return adapter(obj)
