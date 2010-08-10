#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
Zope2-related utility functions.

$Id$
"""

from zope.app.keyreference.interfaces import IKeyReference


def moveKeyReference(intIds, obj):
    """ Make sure entry in intIds utility is updated after a move or rename.
    """
    key = IKeyReference(obj, None)
    if key is not None:
        try:
            uid = intIds.getId(obj)
        except KeyError:
            return
        if uid is not None:
            intIds.refs[uid] = key
            intIds.ids[key] = uid

