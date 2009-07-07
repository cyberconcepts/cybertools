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
A simple caching mechanism.

$Id$
"""

from cybertools.util.date import getTimeStamp

INVALID = object()


class CacheManager(dict):

    pass

manager = CacheManager()


class CacheItem(object):

    def __init__(self, identifier, value=INVALID, lifetime=3600):
        self.identifier = identifier
        self.lifetime = lifetime
        self.set(value)

    def set(self, value):
        self.value = value
        self.modified = getTimeStamp()

    def get(self):
        self.check()
        return self.value

    def check(self):
        if getTimeStamp() - self.modified > self.lifetime:
            self.value = INVALID


def cache(getIdentifier, lifetime=3600):
    def _cache(fct):
        def __cache(*args, **kw):
            id = getIdentifier(*args)
            item = manager.setdefault(id, CacheItem(id, lifetime=lifetime))
            value = item.get()
            if value is INVALID:
                value = fct(*args, **kw)
                item.set(value)
            return value
        return __cache
    return _cache
