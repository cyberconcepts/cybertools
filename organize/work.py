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
Planning and recording activities (work items).

$Id$
"""

from zope.component import adapts
from zope.interface import implementer, implements

from cybertools.organize.interfaces import IWorkItem
from cybertools.stateful.base import Stateful
from cybertools.stateful.definition import StatesDefinition
from cybertools.stateful.definition import State, Transition
from cybertools.stateful.interfaces import IStatesDefinition


@implementer(IStatesDefinition)
def workItemStates():
    return StatesDefinition('workItemStates',
        State('created', 'created', ('assign', 'cancel',), color='red'),
        State('assigned', 'assigned', ('start', 'finish', 'cancel', 'transfer'),
              color='yellow'),
        State('running', 'running', ('finish',), color='green'),
        State('finished', 'finished', (), color='blue'),
        State('transferred', 'transferred', (), color='grey'),
        State('cancelled', 'cancelled', (), color='grey'),
        Transition('assign', 'assign', 'assigned'),
        Transition('start', 'start', 'running'),
        Transition('finish', 'finish', 'finished'),
        Transition('transfer', 'transfer', 'transferred'),
        Transition('cancel', 'cancel', 'cancelled'),
        initialState='created')


class WorkItem(Stateful):

    implements(IWorkItem)

    statesDefinition = 'organize.workItemStates'

