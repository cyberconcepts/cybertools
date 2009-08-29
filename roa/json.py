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
Adapter(s)/view(s) for providing object attributes and other data in JSON format.

$Id$
"""

from cybertools.util import json


class JSONView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return json.dumps(self.context.__dict__.keys())

    def traverse(self, name):
        # To be implemented by subclass
        print '*** traversing', self.context, name
        return self.context
