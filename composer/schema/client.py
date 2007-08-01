#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
Client implementations.

$Id$
"""

from persistent import Persistent
from zope.component import adapts
from zope.interface import implements

from cybertools.composer.schema.interfaces import IClient
from cybertools.composer.schema.interfaces import IClientManager, IClientFactory


class Client(Persistent):

    implements(IClient)

    def __init__(self, manager=None):
        self.manager = manager


class ClientFactory(object):

    implements(IClientFactory)
    adapts(IClientManager)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return Client(self.context)

