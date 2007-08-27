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


$Id$
"""


def getNotifier(method):
    if isinstance(method, Notifier):
        return method
    return Notifier(method)


class Notifier(object):

    def __init__(self, method):
        self.method = method
        obj = method.im_self or method.im_class
        name = method.im_func.func_name
        setattr(obj, name, self)
        self.beforeSubs = []
        self.afterSubs = []

    def __get__(self, instance, cls=None):
        return BoundNotifier(self, instance)

    def __call__(self, *args, **kw):
        for sub, sargs, skw in self.beforeSubs:
            sub(None, *sargs, **skw)
        result = self.method(*args, **kw)
        for sub, aargs, akw in self.afterSubs:
            sub(result, *aargs, **akw)
        return result

    def subscribe(self, before, after, *args, **kw):
        if before is not None:
            self.beforeSubs.append((before, args, kw))
        if after is not None:
            self.afterSubs.append((after, args, kw))


class BoundNotifier(object):

    def __init__(self, context, instance):
        self.context = context
        self.instance = instance

    def __call__(self, *args, **kw):
        for sub, sargs, skw in self.context.beforeSubs:
            sub(None, *sargs, **skw)
        result = self.context.method(self.instance, *args, **kw)
        for sub, aargs, akw in self.context.afterSubs:
            sub(result, *aargs, **akw)
        return result

    def subscribe(self, before, after, *args, **kw):
        self.context.subscribe(before, after, *args, **kw)

