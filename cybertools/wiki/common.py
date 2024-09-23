# cybertools.wiki.common

""" Common basic generic stuff.
"""

from zope.interface import implementer

from cybertools.wiki.interfaces import IWebResource


protocols = set(['dav', 'file', 'ftp', 'http', 'https', 'javascript',
                 'mailto', 'sftp', 'smb'])


@implementer(IWebResource)
class ExternalPage(object):

    def __init__(self, uid):
        self.uid = uid

    def getUid(self):
        return self.uid

    def getURI(self, request):
        return self.uid

