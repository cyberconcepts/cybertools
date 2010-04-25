#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Base implementation for import adapters.

$Id$
"""

from cStringIO import StringIO
from logging import getLogger

from zope import component
from zope.interface import implements
from zope.cachedescriptors.property import Lazy

from cybertools.external.interfaces import IReader, ILoader


class BaseReader(object):

    implements(IReader)

    def __init__(self, context):
        self.context = context

    def read(self, input):
        return []


class BaseLoader(object):

    implements(ILoader)

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
