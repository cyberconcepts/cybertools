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
Working transparently with the R statistics package.

$Id$
"""

import os
import rpy
from rpy import r
from zope.proxy import removeAllProxies


class RWrapper(object):

    def __init__(self, context):
        self.context = context

    def __getattr__(self, attr):
        value = getattr(self.context, attr)
        return removeAllProxies(value)

    def __call__(self, *args, **kw):
        value = self.context.__call__(*args, **kw)
        value = removeAllProxies(value)
        return RWrapper(value)


rx = RWrapper(r)

with_mode = RWrapper(rpy.with_mode)
#as_py = RWrapper(rpy.as_py)


def graphics(*args, **kw):
    filename = os.tempnam()
    rc = r.GDD(filename, *args, **kw)
    return filename + '.jpg', rc

