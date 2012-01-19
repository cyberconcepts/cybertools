#
#  Copyright (c) 2012 Helmut Merz helmutm@cy55.de
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
Iterator and generator utilities.
"""

from itertools import islice


class BatchIterator(object):

    def __init__(self, data, limit=20, start=0):
        self.data = iter(data)
        self.limit = limit
        self.start = start
        self.count = 0
        self.batch = 0
        self.exhausted = False

    def __iter__(self):
        return self

    def next(self):
        if self.count >= (self.batch + 1) * self.limit:
            raise StopIteration
        if self.start:
            for i in islice(self.data, 0, self.start*self.limit):
                pass
            self.start = 0
        self.count += 1
        try:
            return self.data.next()
        except StopIteration:
            self.exhausted = True
            raise

    def advance(self, batches=1):
        self.batch += batches
        return not self.exhausted
