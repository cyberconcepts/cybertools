# cybertools.stateful.base

""" Basic implementations for stateful objects and adapters.
"""

from persistent.interfaces import IPersistent
from persistent.mapping import PersistentMapping
from zope import component
from zope.component import adapts
from zope.interface.interfaces import ObjectEvent
from zope.event import notify
from zope.interface import implementer

from cybertools.stateful.definition import statesDefinitions
from cybertools.stateful.interfaces import IStateful, IStatefulIndexInfo
from cybertools.stateful.interfaces import ITransitionEvent


@implementer(IStateful)
class Stateful(object):

    statesDefinition = 'default'
    state = None

    def getState(self):
        if self.state is None:
            self.state = self.getStatesDefinition().initialState
        return self.state

    def getStateObject(self):
        states = self.getStatesDefinition().states
        if self.getState() not in states:
            self.state = self.getStatesDefinition().initialState
        return states[self.state]

    def doTransition(self, transition, historyInfo=None):
        sd = self.getStatesDefinition()
        previousState = self.getState()
        if isinstance(transition, str):
            sd.doTransitionFor(self, transition)
            self.notify(transition, previousState)
            return
        available = [t.name for t in sd.getAvailableTransitionsFor(self)]
        for tr in transition:
            if tr in available:
                sd.doTransitionFor(self, tr)
                self.notify(tr, previousState)
                return
        raise ValueError("None of the transitions '%s' is available for state '%s'."
                                % (repr(transition), self.getState()))

    def getAvailableTransitions(self):
        sd = self.getStatesDefinition()
        return sd.getAvailableTransitionsFor(self)

    def getAvailableTransitionsForUser(self):
        return self.getAvailableTransitions()

    def getStatesDefinition(self):
        return statesDefinitions.get(self.statesDefinition, None)

    def checkActors(self, actors):
        if not actors:
            return True
        stfActors = self.getActors()
        if stfActors is None:
            return True
        for actor in actors:
            if actor in stfActors:
                return True
        return False

    def getActors(self):
        return None

    def notify(self, transition, previousState):
        """ To be implemented by subclass.
        """


class StatefulAdapter(Stateful):
    """ An adapter for persistent objects to make them stateful.
    """

    adapts(IPersistent)

    statesAttributeName = '__stateful_states__'

    request = None

    def __init__(self, context):
        self.context = context
        self.msgFactory = self.getStatesDefinition().msgFactory

    def getState(self):
        statesAttr = getattr(self.context, self.statesAttributeName, {})
        return statesAttr.get(self.statesDefinition,
                              self.getStatesDefinition().initialState)
    def setState(self, value):
        statesAttr = getattr(self.context, self.statesAttributeName, None)
        if statesAttr is None:
            statesAttr = PersistentMapping()
            setattr(self.context, self.statesAttributeName, statesAttr)
        statesAttr[self.statesDefinition] = value
    state = property(getState, setState)

    def notify(self, transition, previousState):
        transObject = self.getStatesDefinition().transitions[transition]
        notify(TransitionEvent(self.context, transObject, previousState, self.request))


@implementer(IStatefulIndexInfo)
class IndexInfo(object):

    availableStatesDefinitions = []     # to be overwritten by subclass!

    def __init__(self, context):
        self.context = context

    @property
    def tokens(self):
        for std in self.availableStatesDefinitions:
            stf = component.getAdapter(self.context, IStateful, name=std)
            yield ':'.join((std, stf.state))


# event

@implementer(ITransitionEvent)
class TransitionEvent(ObjectEvent):

    def __init__(self, obj, transition, previousState, request=None):
        super(TransitionEvent, self).__init__(obj)
        self.transition = transition
        self.previousState = previousState
        self.request = request
