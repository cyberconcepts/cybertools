#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
Transaction management.

$Id$
"""

from zope.interface import implements
from cybertools.brain.interfaces import ITransaction


class Transaction(object):

    implements(ITransaction)

    def __init__(self):
        self.states = {}

    def setState(self, neuron, state):
        self.states[neuron] = state

    def getState(self, neuron):
        return self.states.get(neuron, neuron.state)


transactions = []

def getTransaction(transaction=None, create=True):
    if transaction is None:
        if transactions:
            transaction = transactions[0]
        elif create:
            transaction = Transaction()
            transactions.append(transaction)
        else:
            return None
    return transaction

def endTransaction(transaction=None):
    if transaction is None:
        if transactions:
            del transactions[0]
    else:
        if transaction in transactions:
            del transactions[transactions.index(transaction)]

