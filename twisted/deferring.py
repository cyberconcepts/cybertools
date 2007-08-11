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
Objects that defer attribute access.

$Id$
"""

from twisted.internet import reactor
from twisted.internet.defer import Deferred


class Deferring(Deferred):

    def __init__(self, context):
        self.context = context
        Deferred.__init__(self)

    def __getattr__(self, attr):
        d = Deferring(self)
        reactor.callLater(0, d.getattr, self, attr)
        return d

    def __call__(self, *args, **kw):
        d = Deferring(None)
        reactor.callLater(0, d.call, self, *args, **kw)
        return d

    def __repr__(self):
        return '<Deferring on %s>' % repr(self.context)

    __str__ = __repr__

    def makeCallback(self, method, *args, **kw):
        #print '*** makeCallback', self, method, args, kw
        def cb(result, method=method, args=args, kw=kw):
            value = method(result, *args, **kw)
            #print '*** cb', self, result, method, args, kw, value
            self.callback(value)
        return cb

    def getattr(self, deferring, attr):
        ctx = deferring.context
        if isinstance(ctx, Deferring):
            ctx.addCallback(self.makeCallback(self.getattr, attr))
        else:
            value = getattr(deferring.context, attr)
            self.context = value
            self.callback(value)

    def call(self, deferring, *args, **kw):
        ctx = deferring.context
        value = ctx(*args, **kw)
        self.context = value
        self.callback(value)

