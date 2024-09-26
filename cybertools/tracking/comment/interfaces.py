# cybertools.tracking.comment.interfaces

""" Interface definitions for comments - discussions - forums.
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
        default=b'text/restructured',
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

