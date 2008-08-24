#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
Common functionality.

$Id$
"""


class RelationSet(object):

    def __init__(self, parent, attributeName):
        self.parent = parent
        self.attributeName = attributeName
        self.data = {}

    def add(self, related):
        self.data[related.name] = related
        relatedData = getattr(related, self.attributeName).data
        relatedData[self.parent.name] = self.parent

    def remove(self, related):
        name = related.name
        del self.data[name]
        relatedData = getattr(related, self.attributeName).data
        del relatedData[self.parent.name]

    def __iter__(self):
        for obj in self.data.values():
            yield obj
