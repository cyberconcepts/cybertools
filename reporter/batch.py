#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
Batching implementation.

$Id$
"""

import itertools
from zope.interface import implements
from interfaces import IBatch


class Batch(object):

    lastPage = False

    def __init__(self, iterable, pageIndex=0, size=20, overlap=0, orphan=0):
        self.iterable = list(iterable)
        self.pageIndex = pageIndex
        self.start = pageIndex * (size - overlap)
        self.size = self.actualSize = size
        self.overlap = overlap
        self.orphan = orphan
        length = len(self.iterable)
        self.pages = range(0, length, size-overlap)
        lastPage = self.pages[-1]
        lastLen = length - lastPage
        if lastLen <= orphan + overlap:
            del self.pages[-1]
            if pageIndex == len(self.pages) - 1: #we're on the last page
                self.actualSize = size + lastLen  #take over the orphans
        if pageIndex >= len(self.pages) or pageIndex < 0:
            self.items = []
        else:
            self.items = self.iterable[self.start:self.start+self.actualSize]

    def __getitem__(self, idx):
        return self.items[idx]

    def next(self):
        for item in self.items:
            yield item

    def __len__(self):
        return len(self.items)

    def getIndexRelative(self, ridx=1):
        idx = self.pageIndex + ridx
        if idx < 0:
            return 0
        if idx >= len(self.pages):
            return len(self.pages) - 1
        return idx
        
    def getIndexAbsolute(self, idx=0):
        if idx < 0:
            idx = len(self.pages) + idx
        if idx < 0 or idx >= len(self.pages):
            return None
        return idx

