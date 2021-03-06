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

from zope.interface import implements
from cybertools.util import json


class JSONView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    # application methods, to be implemented by subclass

    def getData(self, **kw):
        return {}

    def putData(self, data):
        return True

    def createObject(self, name, data):
        return True

    # protocol methods

    def get(self):
        print '*** GET', self.context
        self.setHeader()
        return json.dumps(self.getData())

    def put(self):
        print '*** PUT', self.context, self.getBody()
        self.setHeader()
        result = self.putData(self.getBody())
        return json.dumps(dict(ok=result))

    def create(self, name):
        print '*** create (PUT)', self.context, name, self.getBody()
        self.setHeader(201)
        result = self.createObject(name, self.getBody())
        return json.dumps(dict(ok=result, id=name))

    # helper methods

    def getBody(self):
        inp = self.request.stdin
        inp.seek(0)
        return inp.read()

    def setHeader(self, status=None):
        response = self.request.response
        if status:
            response.setStatus(status)
        response.setHeader('Content-Type', 'application/json')
