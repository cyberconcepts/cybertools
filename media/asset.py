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
Media asset file adapter.

Authors: Johann Schimpf, Erich Seifert.

$Id$
"""

from logging import getLogger
import mimetypes
import os, re, sys

from zope import component
from zope.interface import implements
from cybertools.media.interfaces import IMediaAsset, IFileTransform
from cybertools.media.piltransform import PILTransform
from cybertools.storage.filesystem import FileSystemStorage

TRANSFORM_STATEMENT = re.compile(r"\s*(\+?)([\w]+[\w\d]*)\(([^\)]*)\)\s*")

DEFAULT_FORMATS = {
    "image": "image/jpeg"
}

def parseTransformStatements(txStr):
    """ Parse statements in transform chain strings."""
    statements = TRANSFORM_STATEMENT.findall(txStr)
    return statements

def getMimeBasetype(mimetype):
    return mimetype.split("/",1)[0]

def getMimetypeExt(mimetype):
    exts = mimetypes.guess_all_extensions(mimetype)
    return exts and exts[-1] or ""


class MediaAssetFile(object):
    """ Class for extracting metadata from assets and to create transformed
        variants using file representations in subdirectories.
    """

    implements(IMediaAsset)

    def __init__(self, dataPath, rules, contentType):
        self.dataPath = dataPath
        self.rules = rules
        self.mimeType = contentType

    def getData(self, variant=None):
        if variant is None:
            return self.getOriginalData()
        path = self.getPath(variant)
        if not os.path.exists(path):
            getLogger('cybertools.media.asset.MediaAssetFile').warn(
                'Media asset directory %r not found.' % path)
            self.transform()
            #return self.getOriginalData()
        f = open(path, 'rb')
        data =f.read()
        f.close()
        return data

    def getContentType(self, variant=None):
        contentType = self.getMimeType()
        if variant is None:
            return contentType
        outputFormat = None
        # Scan all statements for a defintion of an output format
        optionsstr = self.rules.get(variant)
        if optionsstr:
            statements = parseTransformStatements(optionsstr)
            for prefix, command, args in statements:
                if command == "output":
                    outputFormat = args
                    break
        # Return default type if no defintion was found
        if not outputFormat:
            baseType = getMimeBasetype(contentType)
            return DEFAULT_FORMATS.get(baseType) or contentType
        return outputFormat

    def transform(self, rules=None):
        if rules is None:
            rules = self.rules
        for variant, commands in rules.items():
            self.createVariant(variant, commands)

    def createVariant(self, variant, commands):
        oldassetdir = self.getDataPath()
        # get or create output directory
        path = self.getPath(variant)
        assetdir = os.path.dirname(path)
        if not os.path.exists(assetdir):
            os.makedirs(assetdir)
        excInfo = None  # Save info of exceptions that may occur
        try:
            mediaFile = PILTransform()
            mediaFile.open(oldassetdir)
            statements = parseTransformStatements(commands)
            for prefix, command, args in statements:
                if command == "rotate":
                    rotArgs = args.split(",")
                    angle = float(rotArgs[0])
                    resize = False
                    if len(rotArgs) > 1:
                       resize = bool(int(rotArgs[1]))
                    mediaFile.rotate(angle, resize)
                elif command == "color":
                    mode = args
                    mediaFile.color(mode)
                elif command == "crop":
                    dims = [float(i) for i in args.split(",")]
                    if dims and (2 <= len(dims) <= 4):
                        mediaFile.crop(*dims)
                elif command == "size":
                    size = [int(i) for i in args.split(",")]
                    if size:
                        mediaFile.resize(*size)
            outputFormat = self.getContentType(variant)
            mediaFile.save(path, outputFormat)
        except Exception, e:
            excInfo = sys.exc_info()
        # Handle exceptions that have occured during the transformation
        # in order to provide information on the affected asset
        if excInfo:
            eType, eValue, eTraceback = excInfo  # Extract exception information
            raise eType("Error transforming asset '%s': %s" %
                        (oldassetdir, eValue)), None, eTraceback

    def getPath(self, variant):
        pathOrig = self.getDataPath()
        dirOrig, fileOrig = os.path.split(pathOrig)
        pathTx = os.path.join(dirOrig, variant, self.getName())
        outputFormat = self.getContentType(variant)
        #outputExt = getMimetypeExt(outputFormat)
        basePath = os.path.splitext(pathTx)[0]
        for ext in mimetypes.guess_all_extensions(outputFormat):
            pathTx = basePath + ext
            if os.path.exists(pathTx):
                return pathTx
        return pathTx

    def getMimeType(self):
        return self.mimeType

    def getName(self):
        return os.path.split(self.getDataPath())[1]

    def getDataPath(self):
        return self.dataPath

    def getOriginalData(self):
        f = self.getDataPath().open()
        data = f.read()
        f.close()
        return data
