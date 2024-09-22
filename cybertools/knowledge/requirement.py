# cybertools.knowledge.requirement

""" Represent positions that require certain knowledge.
"""

from zope.interface import implementer
from cybertools.knowledge.interfaces import IRequirementProfile


@implementer(IRequirementProfile)
class RequirementProfile(object):

    def __init__(self):
        self._requirements = {}

    def getRequirements(self):
        return self._requirements

    def requires(self, obj):
        self._requirements[obj] = True

    def removeRequirement(self, obj):
        del self._requirements[obj]

