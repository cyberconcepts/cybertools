#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
Basic implementations for configuration options

$Id$
"""

from zope.interface import implements

from cybertools.meta.interfaces import IOptions, IConfigurator
from cybertools.meta.namespace import AutoNamespace, Executor, ExecutionError


class Options(AutoNamespace):

    implements(IOptions)


class Configurator(object):

    implements(IConfigurator)

    def __init__(self, context):
        self.context = context

    def load(self, text=None, file=None):
        if file is not None:
            if hasattr(file, 'read'):
                text = file.read()
            else:   # must be a file name
                f = open(file, 'r')
                text = f.read()
                f.close()
        result = Executor(self.context).execute(text)
        if result:
            raise ExecutionError('\n' + result)

    def dump(self, file=None):
        text = str(options)
        if file is not None:
            if hasattr(file, 'write'):
                file.write(text)
            else:   # must be a file name
                f = open(file, 'w')
                f.write(text)
                f.close()
        return text

