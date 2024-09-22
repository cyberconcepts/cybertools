# cybertools.organize.task

""" Task management classes.
"""

from zope.component import adapts
from zope.interface import implementer

from cybertools.organize.interfaces import ITask


@implementer(ITask)
class Task(object):

    pass

