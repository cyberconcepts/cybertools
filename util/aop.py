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
    if isinstance(method, (Notifier, BoundNotifier)):
        return method
    if method.im_self is not None:
        name = method.im_func.func_name
        classMethod = getattr(method.im_class, name)
        if not isinstance(classMethod, Notifier):
            classMethod = Notifier(classMethod)
            setattr(method.im_class, name, classMethod)
        notifier = BoundNotifier(classMethod, method.im_self)
        setattr(method.im_self, name, notifier)
        return notifier
    return Notifier(method)


class Notifier(object):

    def __init__(self, method):
        self.method = method
        obj = method.im_self or method.im_class
        name = self.name = method.im_func.func_name
        setattr(obj, name, self)
        self.beforeSubs = []
        self.afterSubs = []

    def __get__(self, instance, cls=None):
        if instance is None:
            # class-level access
            return self
        existing = instance.__dict__.get(self.name)
        if isinstance(existing, BoundNotifier):
            # the instance's method is already wrapped
            return existing
        notifier = BoundNotifier(self, instance)
        setattr(instance, self.name, notifier)
        return notifier

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
        self.beforeSubs = []
        self.afterSubs = []

    def __call__(self, *args, **kw):
        context = self.context
        for sub, sargs, skw in self.beforeSubs + context.beforeSubs:
            sub(None, *sargs, **skw)
        result = context.method(self.instance, *args, **kw)
        for sub, aargs, akw in self.afterSubs + context.afterSubs:
            sub(result, *aargs, **akw)
        return result

    def subscribe(self, before, after, *args, **kw):
        if before is not None:
            self.beforeSubs.append((before, args, kw))
        if after is not None:
            self.afterSubs.append((after, args, kw))

