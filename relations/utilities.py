#
#  Copyright (c) 2005 Helmut Merz helmutm@cy55.de
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
Implementation of the utilities needed for the relations package.

$Id$
"""

from zope.interface import implements
from zope.app import zapi

class RelationsRepository(Persistent, Contained):
    """ Local utility for storing relations.
    """

    def add(self, relation):
        return 'bla'

    def remove(self, relation):
        pass
        

class RelationsRegistry(Persistent, Contained):
    """ Local utility for registering (cataloguing) and searching relations.
    """

    def register(self, relation):
        pass
    
    def unregister(relation):
        pass
    
    def query(**kw):
        return []

