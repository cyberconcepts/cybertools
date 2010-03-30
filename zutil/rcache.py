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
A simple mechanism for caching values in the request.

$Id$
"""


INVALID = object()


def caching(self, method, id):
    annot = self.request.annotations
    item = annot.setdefault('cybertools.util.rcache', {})
    value = item.get(id, INVALID)
    if value is INVALID:
        value = method()
        item[id] = value
    return value


def requestCache(method):
    def _cache(self):
        return caching(self, method, method.__name__)
    return _cache

rcache = requestCache


class requestCacheProperty(object):

    def __init__(self, func):
        self.func = func

    def __get__(self, inst, class_):
        if inst is None:
            return self
        id = self.func.__name__
        value = caching(inst, self.func, id)
        inst.__dict__[id] = value
        return value

rcacheproperty = requestCacheProperty
