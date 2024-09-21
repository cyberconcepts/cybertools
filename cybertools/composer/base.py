# cybertools.composer.base

""" Basic classes for complex template structures.
"""

from zope.interface import implementer

from cybertools.composer.interfaces import IComponent, IElement, ICompound
from cybertools.composer.interfaces import ITemplate
from cybertools.util.jeep import Jeep


@implementer(IComponent)
class Component(object):

    pass


@implementer(IElement)
class Element(Component):

    pass


@implementer(ICompound)
class Compound(Component):

    componentStorage = Jeep

    def __init__(self):
        self.parts = self.componentStorage()


@implementer(ITemplate)
class Template(object):

    componentStorage = Jeep
    components = None

    def __init__(self):
        if self.componentStorage is not None:
            self.components = self.componentStorage()

