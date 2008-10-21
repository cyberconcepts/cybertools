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
Media asset management interface definitions.

$Id$
"""

from zope.interface import Interface, Attribute

from loops.interfaces import IExternalFile


class IMediaAsset(Interface):

    def getData(variant=None):
        """ Return the binary data of the media asset or one of its variants.
        """

    def getContentType(variant=None):
        """ Return the mime-formatted content type of the media asset
            or one of its variants.
        """

    def transform(rules):
        """ Generate user-defined transformed variants of the media asset
            according to the rules given.
        """


class IFileTransform(Interface):
    """ Transformations using files in the filesystem.
    """

    def open(path):
        """ Open the image under the given filename.
        """

    def save(path, mimetype):
        """ Save the image under the given filename.
        """

    def rotate(rotangle):
        """ Return a copy of an image rotated the given number of degrees
            counter clockwise around its centre.
        """

    def color(mode):
        """ Create image with specified color mode (e.g. 'greyscale').
        """

    def crop(relWidth, relHeight, alignX=0.5, alignY=0.5):
        """ Return a rectangular region from the current image. The box is defined
            by a relative width and a relative height defining the crop aspect
            as well as a horizontal (x) and a verical (y) alignment parameters.
        """

    def resize(width, height):
        """ Modify the image to contain a thumbnail version of itself, no
            larger than the given size.
        """
