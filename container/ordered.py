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
Ordered container implementation.

$Id$
"""

from zope.app import zapi
from zope.app.container.ordered import OrderedContainer as BaseOrderedContainer
from zope.cachedescriptors.property import Lazy
from zope.app.container.browser.contents import JustContents


class OrderedContainerView(JustContents):
    """ A view providing the necessary methods for moving sub-objects
        within an ordered container.
    """

    @Lazy
    def orderable(self):
        return len(self.context) > 1

    def checkMoveAction(self):
        request = self.request
        for var in request:
            if var.startswith('move_'):
                delta = request.get('delta', 1)
                ids = request.get('ids', [])
                if ids:
                    m = getattr(self, var, None)
                    if m:
                        m(ids, delta)
                return

    def move_down(self, ids=[], delta=1):
        self.context.updateOrder(
                moveByDelta(self.context.keys(), ids, int(delta)))

    def move_up(self, ids=[], delta=1):
        self.context.updateOrder(
                moveByDelta(self.context.keys(), ids, -int(delta)))

    def move_bottom(self, ids=[], delta=0):
        self.context.updateOrder(
                moveByDelta(self.context.keys(), ids, len(self.context)))

    def move_top(self, ids=[], delta=0):
        self.context.updateOrder(
                moveByDelta(self.context.keys(), ids, -len(self.context)))


def moveByDelta(objs, toMove, delta):
    """ Return the list given by objs resorted in a way that the elements
        of toMove (which must be in the objs list) have been moved by delta.
    """
    result = [obj for obj in objs if obj not in toMove]
    if delta < 0:
        objs = list(reversed(objs))
        result.reverse()
    toMove = sorted(toMove, lambda x,y: cmp(objs.index(x), objs.index(y)))
    for element in toMove:
        newPos = min(len(result), objs.index(element) + abs(delta))
        result.insert(newPos, element)
    if delta < 0:
        result.reverse()
    return result

