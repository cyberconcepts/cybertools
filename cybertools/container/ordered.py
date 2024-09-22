# cybertools.util.container.ordered

""" Ordered container implementation.
"""

from zope.app.container.ordered import OrderedContainer as BaseOrderedContainer
from zope.cachedescriptors.property import Lazy
from zope.i18nmessageid import ZopeMessageFactory as _
from zope.interface import Interface
from base import ContainerView


class OrderedContainerView(ContainerView):
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
                    getattr(self, var, None)(ids, delta)
                else:
                    self.error = _("You didn't specify any ids to move.")
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
    """ Return the list given by objs re-ordered in a way that the elements
        of toMove (which must be in the objs list) have been moved by delta.
    """
    result = [obj for obj in objs if obj not in toMove]
    if delta < 0:
        objs = list(reversed(objs))
        result.reverse()
    toMove = sorted(toMove, key=lambda x: objs.index(x))
    for element in toMove:
        newPos = min(len(result), objs.index(element) + abs(delta))
        result.insert(newPos, element)
    if delta < 0:
        result.reverse()
    return result

