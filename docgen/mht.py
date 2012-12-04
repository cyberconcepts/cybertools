#
#  Copyright (c) 2012 Helmut Merz helmutm@cy55.de
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
Working with MHT Files.
"""

from email import message_from_string
#from email.multipart import MIMEMultipart


class MHTFile(object):

    #encoding = 'UTF-8'
    #encoding = 'ISO8859-15'
    encoding = 'Windows-1252'
    bodyMarker = 'lxdoc_body'
    indexes = dict(body=2, filelist=-2)


    def __init__(self, data):
        self.data = data
        self.msg = message_from_string(data)
        self.boundary = self.msg.get_boundary()
        self.parts = data.split(self.boundary)
        #print '***', len(self.parts)
        #for idx, part in enumerate(self.msg.walk()):
        #    print '***', idx, part['Content-Location'], part.get_content_type()

    def addImage(self, imagePath):
        pass

    def setBody(self, body):
        content = body.encode(self.encoding)
        bodyIndex = self.indexes['body']
        baseDocument = self.parts[bodyIndex]
        self.parts[bodyIndex] =  baseDocument.replace(self.bodyMarker, 
                                        self.quopri(content))

    def asString(self):
        #msg = MIMEMultipart('related')
        return self.boundary.join(self.parts)

    def quopri(self, s):
        return s.replace('="', '=3D"')

