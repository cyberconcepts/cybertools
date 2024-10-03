# cybertools.xedit.handler

""" HTTP method handler.
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
        print(self.request['wsgi.input'].read())
