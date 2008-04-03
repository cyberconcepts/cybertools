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
Common stuff.

$Id$
"""

from cybertools.util.jeep import Jeep


class JobState(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def hasError(self):
        return self.value < 0

    def hasFinished(self):
        return (self.value <= states.aborted.value or
                self.value >= states.completed.value)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<JobState %s>' % self.name


states = Jeep([JobState(n, v) for n, v in
                (('initialized', 0), ('scheduled', 1), ('submitted', 2),
                 ('running', 3), ('completed', 4), ('aborted', -1))])
