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

import base64
import email
import os


class MHTFile(object):

    #encoding = 'UTF-8'
    #encoding = 'ISO8859-15'
    encoding = 'Windows-1252'
    bodyMarker = 'lxdoc_body'
    indexes = dict(body=2, filelist=-2)

    imageTemplate = ('\n'
        'Content-Location: file:///C:/AF2749EC/%(docname)s-Dateien/$(imgname)s\n'
        'Content-Transfer-Encoding: base64\n'
        'Content-Type: %(ctype)s\n\n%(imgdata)s\n\n')

    filelistItemTemplate = ' <o:File HRef=3D"%s"/>\n'
    filelistPattern ='<o:File HRef=3D"filelist.xml"/>'

    def __init__(self, data, body):
        self.data = data
        self.msg = email.message_from_string(data)
        self.boundary = self.msg.get_boundary()
        self.parts = data.split(self.boundary)
        self.body = body
        self.htmlDoc = HTMLDoc(body)
        self.lastImageNum = 0
        self.imageMappings = []
        #print '***', len(self.parts)
        for idx, part in enumerate(self.msg.walk()):
        #    print '***', idx, , part.get_content_type()
            if idx == 1:
                docPath = part['Content-Location']
        self.documentName = docPath
        # TODO: collect existing images to provide consistent naming

    def getImageRefs(self):
        return self.htmlDoc.getImageRefs()

    def addImage(self, imageData, path='image001.jpg', contentType='image/jpeg'):
        flpos = self.indexes['filelist']
        # TODO: get contentType from path
        # TODO: generate name, update self.imageMappings
        name = path
        vars = dict(docname=self.documentName, imgname=name, ctype=contentType,
                    imgdata=base64.encodestring(imageData))
        content = self. imageTemplate % vars
        self.parts.insert(flpos, content)
        filelistRep = (self.filelistItemTemplate % name) + self.filelistPattern
        filelist = self.parts[flpos]
        self.parts[flpos] = filelist.replace(self.filelistPattern, filelistRep)


    def insertBody(self):
        # self.htmlDoc.updateImageRefs(self.imageMappings)
        # TODO: convert changed self.htmlDoc to new body
        content = self.body.encode(self.encoding)
        bodyIndex = self.indexes['body']
        baseDocument = self.parts[bodyIndex]
        self.parts[bodyIndex] =  baseDocument.replace(self.bodyMarker, 
                                        self.quopri(content))

    def asString(self):
        return self.boundary.join(self.parts)

    def quopri(self, s):
        return s.replace('="', '=3D"')


class HTMLDoc(object):

    def __init__(self, data):
        self.data = data

    def getImageRefs(self):
        return []

    def updateImageRefs(self, mappings):
        for old, new in mappings:
            pass

