# cybertools.composer.report.instance

""" Report instance and related classes.
"""

from string import Template
from zope import component
from zope.publisher.browser import TestRequest
try:
    from zope.traversing.browser.absoluteurl import absoluteURL
    zope29 = False
except ImportError:
    from zope.app.traversing.browser.absoluteurl import absoluteURL
    from Acquisition import aq_parent, aq_inner
    zope29 = True

from cybertools.composer.instance import Instance
from cybertools.composer.interfaces import IInstance
from cybertools.util.jeep import Jeep

_not_found = object()


class ReportInstance(Instance):

    template = client = None

    def __init__(self, client, template, manager):
        self.client = client
        self.template = template
        self.manager = manager

    def applyTemplate(self, **kw):
        data = []   # TODO: create result set
        request = data.get('request') or TestRequest()
        return data

