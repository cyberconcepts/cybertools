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
Interface definitions for comments - discussions - forums.

$Id$
"""

from zope.interface import Interface, Attribute
from zope import schema

from cybertools.tracking.interfaces import ITrack


class IComment(ITrack):
    """ A comment is a piece of text provided by a user and related
        to a content object.
        The object the comment is related to is referenced via the
        task id attribute; interdependent comments (i.e. comments in a
        parent/child hierarchy related to the same object share the
        run id; the user name references the user/person that created
        the comment.
    """

    parent = Attribute('The id of the parent comment; None for '
                'the top-level comment.')

    subject = schema.TextLine(
        title=u'Subject',
        description=u'A short informative line of text.',
        default=u'',    # should be taken from the parent
        required=True)
    text = schema.Text(
        title=u'Text',
        description=u'The text of the comment.',
        default=u'',
        required=True)
    contentType = schema.BytesLine(
        title=u'Content Type',
        description=u'Content type (format) of the text field',
        # TODO: provide a source/vocabulary
        default='text/restructured',
        required=True)

    def getChildren(sort='default'):
        """ Returns the immediate children in the order specified by the sort
            argument; the return value is a sequence of track ids.
            The default sorting is by timestamp, newest first.
        """

    def getChildrenTree(sort='default', depth=0):
        """ Returns the children as a tree, in the order specified by
            the sort argument. If depth is greater than 0 only that level
            of children will be returned.
            The return value is a nested sequence of track ids.
        """

