# cybertools.stateful.definition

""" State definition implementation.
"""

from zope.interface import implementer
from cybertools.util.jeep import Jeep

from cybertools.stateful.interfaces import IState, IAction, ITransition
from cybertools.stateful.interfaces import IStatesDefinition


@implementer(IState)
class State(object):

    setSecurity = lambda self, context: None
    icon = None
    color = 'blue'

    def __init__(self, name, title, transitions, **kw):
        self.name = self.__name__ = name
        self.title = title
        self.transitions = transitions
        self.actions = Jeep(kw.pop('actions', []))
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def stateIcon(self):
        return 'cybertools.icons/' + (self.icon or 'led%s.png' % self.color)


@implementer(IAction)
class Action(object):

    allowed = True
    permission = None
    roles = []
    actors = []
    condition = None
    doBefore = []
    schema = None

    def __init__(self, name, title=None, **kw):
        self.name = self.__name__ = name
        self.title = title
        for k, v in kw.items():
            setattr(self, k, v)


@implementer(ITransition)
class Transition(Action):

    def __init__(self, name, title, targetState, **kw):
        super(Transition, self).__init__(name, title, **kw)
        self.targetState = targetState


@implementer(IStatesDefinition)
class StatesDefinition(object):

    initialState = 'started'
    msgFactory = None

    def __init__(self, name, *details, **kw):
        self.name = self.__name__ = name
        self.states = Jeep()
        self.transitions = Jeep()
        msgFactory = kw.get('msgFactory')
        for d in details:
            if ITransition.providedBy(d):
                self.transitions.append(d)
            elif IState.providedBy(d):
                self.states.append(d)
            else:
                raise TypeError('Only states or transitions are allowed here, '
                                'got %s instead.' % repr(d))
            if msgFactory:
                d.title = msgFactory(d.title)
        for k, v in kw.items():
            setattr(self, k, v)

    def doTransitionFor(self, obj, transition):
        if transition not in self.transitions:
            raise ValueError('Transition %s is not available.' % transition)
        trans = self.transitions[transition]
        if not self.isAllowed(trans, obj):
            raise ValueError('Transition %s is not allowed.' % transition)
        if trans not in self.getAvailableTransitionsFor(obj):
            raise ValueError("Transition '%s' is not reachable from state '%s'."
                                    % (transition, obj.getState()))
        if isinstance(trans.doBefore, (list, tuple)):
            for fct in trans.doBefore:
                fct(obj)
        else:
            trans.doBefore(obj)
        obj.state = trans.targetState
        obj.getStateObject().setSecurity(obj)

    def getAvailableTransitionsFor(self, obj):
        state = obj.getState()
        return [self.transitions[t]
                    for t in self.states[state].transitions
                    if self.isAllowed(self.transitions[t], obj)]

    def isAllowed(self, action, obj):
        if not action.allowed:
            return False
        if action.condition and not action.condition(obj):
            return False
        if not obj.checkActors(action.actors):
            return False
        if not self.checkRoles(action.roles, obj):
            return False
        if not self.checkPermission(action.permission, obj):
            return False
        return True

    def checkRoles(self, roles, obj):
        return True

    def checkPermission(self, permission, obj):
        return True


# dummy default states definition

defaultSD = StatesDefinition('default',
    State('started', 'Started', ('finish',)),
    State('finished', 'Finished', ()),
    Transition('finish', 'Finish', 'finished'),
)


# states definitions registry
# TODO: use a utility!!!

statesDefinitions = dict()

def registerStatesDefinition(definition):
    statesDefinitions[definition.name] = definition

registerStatesDefinition(defaultSD)
