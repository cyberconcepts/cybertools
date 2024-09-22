# cybertools.knowledge.provider

""" Knowledge providers provide knowledge.
"""

from zope.interface import implementer
from cybertools.knowledge.interfaces import IKnowledgeProvider


@implementer(IKnowledgeProvider)
class KnowledgeProvider(object):

    def __init__(self):
        self._providedKnowledge = {}

    def getProvidedKnowledge(self):
        return self._providedKnowledge

    def provides(self, obj):
        self._providedKnowledge[obj] = True
        obj._providers.add(self)

    def removeProvidedKnowledge(self, obj):
        del self._providedKnowledge[obj]
        del obj._providers[self]

