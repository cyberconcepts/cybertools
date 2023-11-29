# cybertools.text.interfaces

"""interface definitions for text transformations.
"""

from zope.interface import Interface


class ITextTransform(Interface):

    def __call__(fr):
        """ Transform the content of file fr (readfile) to plain text and
            return the result as unicode.
        """


class IFileTransform(ITextTransform):
    """ A transformation that is performed by calling some external program
        and that typically uses an intermediate disk file.
    """

    def extract(dirname, filename):
        """ Extract text contents from the file specified by ``filename``,
            using some external programm, and return the result as unicode.
            ``dirname`` is the path to a temporary directory that
            usually (but not necessarily) contains the file and may
            be used for creating other (temporary) files if needed.
        """

    def execute(command):
        """ Execute a system command and return the output of the program
            called.
        """

    def checkAvailable(progname, logMessage=''):
        """ Check the availability of the program named ``progname``.
            Return True if available; if ``logMessage`` is given, put this
            as a warning message into the log if the program is not available.
        """
