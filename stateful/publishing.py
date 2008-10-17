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
Definition of a simple publishing workflow.

$Id$
"""

from zope.interface import implementer

from cybertools.stateful.definition import registerStatesDefinition
from cybertools.stateful.definition import StatesDefinition
from cybertools.stateful.definition import State, Transition
from cybertools.stateful.interfaces import IStatesDefinition


@implementer(IStatesDefinition)
def simplePublishing():
    return StatesDefinition('simple_publishing',
        State('private', 'private', ('show', 'archive', 'remove'), color='red'),
        State('draft', 'draft', ('publish', 'hide', 'archive', 'remove'),
              color='blue'),
        State('published', 'published', ('retract', 'archive'), color='green'),
        State('archived', 'archived', ('show', 'remove'), color='grey'),
        State('removed', 'removed', ('show',), icon='cancel.png'),
        Transition('show', 'show', 'draft'),
        Transition('hide', 'hide', 'private'),
        Transition('publish', 'publish', 'published'),
        Transition('retract', 'retract', 'draft'),
        Transition('archive', 'archive', 'archived'),
        Transition('remove', 'remove', 'removed'),
        initialState='draft')
