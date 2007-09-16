#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
interface definitions for the pyscript package.

$Id$
"""

from zope.interface import Interface
from zope import schema
from zope.app.container.constraints import contains
from zope.app.container.interfaces import IContainer
from zope.app.i18n import ZopeMessageFactory as _


class IPythonScript(Interface):
    """Python Script, derived from zope.app.pythonpage.PythonPage.

    The Python Page acts as a simple content type that allows you to execute
    Python in content space. Additionally, if you have a free-standing
    triple-quoted string, it gets converted to a print statement
    automatically.
    """

    parameters = schema.TextLine(
        title=_(u"Parameters"),
        description=_(u"Space-separated list of parameter names."),
        required=False,
        default=u''
    )
    source = schema.SourceText(
        title=_(u"Source"),
        description=_(u"The source of the Python page."),
        required=True,
    )
    contentType = schema.TextLine(
        title=_(u"Content Type"),
        description=_(u"The content type of the script's output (return value "
                "when rendered in the browser)."),
        required=True,
        default=u"text/html",
    )

    def __call__(request, **kw):
        """Execute the script.

        The script will insert the `request` and all `**kw` as global
        variables. Furthermore, the variables `script` and `context` (which is
        the container of the script) will be added.
        """


class IScriptContainer(IContainer):
    """ A container for Python scripts.
    """

    contains(IPythonScript)

    def updateGlobals(globs):
        """ Put additional variable bindings into the globals dictionary.
        """

