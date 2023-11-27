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
HTTP method handler.

$Id$
"""

"""
A real response to a LOCK request would look like this:

HTTP/1.1 200 OK
Content-Type: text/xml; charset="utf-8"
Content-Length: XXXX

<?xml version="1.0" encoding="utf-8" ?>
<d:prop xmlns:d="DAV:">
  <d:lockdiscovery>
    <d:activelock>
      <d:locktype><d:write/></d:locktype>
      <d:lockscope><d:exclusive/></d:lockscope>
      <d:depth>Infinity</d:depth>
      <d:owner>
        <d:href>http://www.contoso.com/~user/contact.htm</d:href>
      </d:owner>
      <d:timeout>Second-345600</d:timeout>
      <d:locktoken>
        <d:href>opaquelocktoken:e71d4fae-5dec-22df-fea5-00a0c93bd5eb1</d:href>
      </d:locktoken>
    </d:activelock>
  </d:lockdiscovery>
</d:prop>
"""

class NullLOCK(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def LOCK(self):
        request = self.request
        #self.printRequest(request)
        response = request.response
        #response.setStatus(200)
        message = '<data>opaquelocktoken:dummy</data>'
        return message

    def UNLOCK(self):
        return ''

    def printRequest(self, request):
        print self.request['wsgi.input'].read()
