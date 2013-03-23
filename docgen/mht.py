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
from cStringIO import StringIO
import email
from PIL import Image
import mimetypes
import os

from cybertools.text.lib.BeautifulSoup import BeautifulSoup, Tag


class MHTFile(object):

    #encoding = 'UTF-8'
    #encoding = 'ISO8859-15'
    encoding = 'Windows-1252'
    bodyMarker = 'lxdoc_body'
    foldernameSuffix = 'Dateien'
    indexes = dict(body=1, filelist=-2)

    path = documentName = None

    imageTemplate = ('\n'
        'Content-Location: %(path)s/%(docname)s-%(suffix)s/%(imgname)s\n'
        'Content-Transfer-Encoding: base64\n'
        'Content-Type: %(ctype)s\n\n%(imgdata)s\n\n')

    filelistItemTemplate = ' <o:File HRef=3D"%s"/>\n'
    filelistPattern =' <o:File HRef=3D"filelist.xml"/>'

    def __init__(self, data, body):
        self.data = data
        self.msg = email.message_from_string(data)
        self.boundary = '--' + self.msg.get_boundary()
        self.parts = data.split(self.boundary)
        self.body = body
        self.htmlDoc = HTMLDoc(body)
        self.lastImageNum = 0
        self.imageMappings = {}
        for idx, part in enumerate(self.msg.walk()):
            docPath = part['Content-Location']
            contentType = part.get_content_type()
            if idx == self.indexes['body']:
                self.path, docname = os.path.split(docPath)
                self.documentName, ext = os.path.splitext(docname)
            if contentType.startswith('image/'):
                self.lastImageNum += 1
        #print '###', self.path, self.documentName, self.lastImageNum

    def getImageRefs(self):
        return self.htmlDoc.getImageRefs()

    def addImage(self, imageData, path):
        image = Image.open(StringIO(imageData))
        width, height = image.size
        contentType, enc = mimetypes.guess_type(path)
        bp, ext = os.path.splitext(path)
        self.lastImageNum += 1
        name = 'image%03i%s' % (self.lastImageNum, ext)
        self.imageMappings[path] = (name, width, height)
        flpos = self.indexes['filelist']
        vars = dict(path=self.path, docname=self.documentName,  
                    suffix=self.foldernameSuffix,
                    imgname=name, ctype=contentType,
                    imgdata=base64.encodestring(imageData))
        content = self. imageTemplate % vars
        self.parts.insert(flpos, str(content))
        filelistRep = (self.filelistItemTemplate % name) + self.filelistPattern
        filelist = self.parts[flpos]
        self.parts[flpos] = str(filelist.replace(self.filelistPattern, filelistRep))


    def insertBody(self):
        path = '-'.join((self.documentName, self.foldernameSuffix))
        self.htmlDoc.updateImageRefs(self.imageMappings, path)
        content = self.htmlDoc.doc.renderContents(self.encoding)
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
        self.doc = BeautifulSoup(data)

    def getImageRefs(self):
        return [img['src'] for img in self.doc('img')]

    def updateImageRefs(self, mappings, path=''):
        for img in self.doc('img'):
            name, width, height = mappings[img['src']]
            imgdata = Tag(self.doc, 'v:imagedata')
            imgdata['src'] = '/'.join((path, name))
            imgdata.isSelfClosing = True
            img.append(imgdata)
            del img['src']
            img['style'] = 'width:%spt;height:%spt' % (width, height)
            img.isSelfClosing = False
            img.name='v:shape'

