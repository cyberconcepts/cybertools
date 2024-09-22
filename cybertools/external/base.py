# cybertools.external.base

""" Base implementation for import adapters.
"""

from io import StringIO
from logging import getLogger

from zope import component
from zope.interface import implementer
from zope.cachedescriptors.property import Lazy

from cybertools.external.interfaces import IReader, ILoader


@implementer(IReader)
class BaseReader(object):

    def __init__(self, context):
        self.context = context

    def read(self, input):
        return []


@implementer(ILoader)
class BaseLoader(object):

    def __init__(self, context):
        self.context = context
        self.changes = []
        self.created = []
        self.errors = []
        self.summary = dict(count=0, new=0, changed=0, errors=0, warnings=0)
        self.transcript = StringIO()
        self.logger = getLogger('Loader')
        self.groups = {}

    def load(self, elements, recur=True):
        self.loadRecursive(elements, recur)
        self.transcript.write('Objects loaded: %(count)i; created: %(new)i, '
                              'changes: %(changed)i, warnings: %(warnings)i, '
                              'errors: %(errors)i\n' % self.summary)

    def loadRecursive(self, elements, recur=True):
        for element in elements:
            element.execute(self)
            if recur and element.subElements is not None:
                self.loadRecursive(element.subElements)
            self.summary['count'] += 1

    def error(self, message):
        self.transcript.write(message.encode('UTF-8') + '\n')
        self.errors.append(message)
        self.summary['errors'] += 1
        self.logger.error(message)

    def warn(self, message):
        self.transcript.write(message.encode('UTF-8') + '\n')
        self.errors.append(message)
        self.summary['warnings'] += 1
        self.logger.warn(message)

    def info(self, message, showInTranscript=True):
        if showInTranscript:
            self.transcript.write(message.encode('UTF-8') + '\n')
        self.logger.info(message)

    def new(self, message=None):
        if message is not None:
            self.transcript.write('Object created: ' + message.encode('UTF-8') + '\n')
            self.created.append(message)
        self.summary['new'] += 1

    def change(self, message=None):
        if message is not None:
            self.transcript.write('Object changed: ' + message.encode('UTF-8') + '\n')
            self.changes.append(message)
        self.summary['changed'] += 1
