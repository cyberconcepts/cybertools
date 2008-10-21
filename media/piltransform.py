#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
Views for displaying media assets.

Authors: Johann Schimpf, Erich Seifert.

$Id$
"""

from logging import getLogger
try:
    import Image
except ImportError:
    getLogger('Asset Manager').warn('Python Imaging Library could not be found.')

from zope.interface import implements

from cybertools.media.interfaces import IMediaAsset, IFileTransform
from cybertools.storage.filesystem import FileSystemStorage


def mimetypeToPIL(mimetype):
    return mimetype.split("/",1)[-1]


class PILTransform(object):
    """ Class for image transformation methods.
        Based on the Python Imaging Library.
    """

    implements(IFileTransform)

    def open(self, path):
        self.im = Image.open(path)

    def rotate(self, angle, resize):
        self.im = self.im.rotate(angle,Image.BICUBIC)

    def color(self, mode):
        if not mode:
            return
        mode = mode.upper()
        if mode == "BITMAP":
            mode = "1"
        elif mode == "GRAYSCALE":
            mode = "L"
        self.im = self.im.convert(mode)

    def crop(self, relWidth, relHeight, alignX=0.5, alignY=0.5):
        alignX = min(max(alignX, 0.0), 1.0)
        alignY = min(max(alignY, 0.0), 1.0)
        w, h = self.im.size
        imgAspect = float(w) / float(h)
        crpAspect = relWidth / relHeight
        if imgAspect >= crpAspect:
            crpWidth = h * crpAspect
            crpHeight = h
        else:
            crpWidth = w
            crpHeight = w / crpAspect
        left = int((w - crpWidth) * alignX)
        upper = int((h - crpHeight) * alignY)
        right = int(left + crpWidth)
        lower = int(upper + crpHeight)
        box = (left, upper, right, lower)
        self.im = self.im.crop(box)

    def resize(self, width, height):
        dims = (width, height)
        self.im.thumbnail(dims, Image.ANTIALIAS)

    def save(self, path, mimetype):
        format = mimetypeToPIL(mimetype)
        self.im.save(path)
