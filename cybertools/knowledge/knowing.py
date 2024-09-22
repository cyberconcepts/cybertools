# cybertools.knowledge.knowing

""" Manage objects (people) who know something.
"""

from zope.interface import implementer
from cybertools.knowledge.interfaces import IKnowing


@implementer(IKnowing)
class Knowing(object):

    def __init__(self):
        self._knowledge = {}

    def getKnowledge(self):
        return self._knowledge

    def knows(self, obj):
        self._knowledge[obj] = True
        obj._knowers.add(self)

    def removeKnowledge(self, obj):
        del self._knowledge[obj]
        del obj._knowers[self]

    def getMissingKnowledge(self, profile):
        knowledge = list(self.getKnowledge())
        missing = []
        toCheck = [k for k in profile.getRequirements() if k not in knowledge]
        while toCheck:
            k = toCheck.pop()
            missing.insert(0, k)
            for d in k.getDependencies():
                if d in knowledge or d in toCheck:
                    continue
                if d in missing:
                # TODO: rearrange missing, but care for cycles...
                    continue
                toCheck.append(d)
        return tuple(missing)

    def getProvidersNeeded(self, profile):
        return ((k, k.getProviders())
                    for k in self.getMissingKnowledge(profile))


