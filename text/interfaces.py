#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
interface definitions for text transformations.

$Id$
"""

from zope.interface import Interface


class ITextTransform(Interface):

    def __call__(f):
        """ Transform the content of file f to plain text and return
            the result as unicode.
        """


class IFileTransform(ITextTransform):
    """ A transformation that uses an intermediate disk file.
    """

    def extract(dirname, filename):
        """ Extract text contents from the file specified by dirnam, filename,
            using some external programm, and return the result as unicode.
        """
