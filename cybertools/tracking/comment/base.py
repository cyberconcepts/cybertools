# cybertools.tracking.comment.base

""" Basic implementation of comments / discussions.
"""

from zope.interface import implementer

from cybertools.tracking.btree import Track
from cybertools.tracking.comment.interfaces import IComment


@implementer(IComment)
class Comment(Track):

    pass
