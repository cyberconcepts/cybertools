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
Report result sets and related classes.

$Id$
"""


class Row(object):

    def __init__(self, context):
        self.context = context

    def __getattr__(self, attr):
        return getattr(self.context, attr)


class ResultSet(object):

    def __init__(self, context, data, rowFactory=Row, sortCriteria=None):
        self.context = context
        self.data = data
        self.rowFactory = rowFactory
        self.sortCriteria = sortCriteria

    def getResult(self):
        result = [self.rowFactory(item) for item in self.data]
        if self.sortCriteria:
            result.sort(key=lambda x: [f.getSortValue(x) for f in self.sortCriteria])
        return result

    def __iter__(self):
        return iter(self.getResult())

