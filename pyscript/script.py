##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Python Page

$Id$
"""

__docformat__ = 'restructuredtext'

import new
import re
from cStringIO import StringIO
from persistent import Persistent
from zope.proxy import removeAllProxies
from zope.security.untrustedpython.builtins import SafeBuiltins
#from zope.security.untrustedpython.rcompile import compile
from zope.traversing.api import getParent, getPath
from zope.app.container.contained import Contained
from zope.interface import implements
from zope.app.i18n import ZopeMessageFactory as _

from cybertools.pyscript.interfaces import IPythonScript, IScriptContainer


import compiler.pycodegen
import RestrictedPython.RCompile
from RestrictedPython.SelectCompiler import ast
from zope.security.untrustedpython.rcompile import RestrictionMutator as BaseRM

unrestricted_objects = ('rpy', 'r')

def compile(text, filename, mode):
    if not isinstance(text, basestring):
        raise TypeError("Compiled source must be string")
    gen = RExpression(text, str(filename), mode)
    gen.compile()
    return gen.getCode()

class RExpression(RestrictedPython.RCompile.RestrictedCompileMode):

    CodeGeneratorClass = compiler.pycodegen.ExpressionCodeGenerator

    def __init__(self, source, filename, mode = "eval"):
        self.mode = mode
        RestrictedPython.RCompile.RestrictedCompileMode.__init__(
            self, source, filename)
        self.rm = RestrictionMutator()

class RestrictionMutator(BaseRM):

    unrestricted_objects = unrestricted_objects

    def visitGetattr(self, node, walker):
        _getattr_name = ast.Name("getattr")
        node = walker.defaultVisitNode(node)
        if node.expr.name in self.unrestricted_objects:
            return node     # no protection
        return ast.CallFunc(_getattr_name,
                            [node.expr, ast.Const(node.attrname)])


class PythonScript(Contained, Persistent):
    """Persistent Python Page - Content Type
    """

    implements(IPythonScript)

    _v_compiled = None

    def __init__(self, source=u'', contentType=u'text/plain'):
        """Initialize the object."""
        super(PythonScript, self).__init__()
        self.source = source
        self.contentType = contentType

    def __filename(self):
        if self.__parent__ is None:
            filename = 'N/A'
        else:
            filename = getPath(self)
        return filename

    def setSource(self, source):
        """Set the source of the page and compile it.

        This method can raise a syntax error, if the source is not valid.
        """
        self.__source = source
        self.__prepared_source = self.prepareSource(source)
        # Compile objects cannot be pickled
        self._v_compiled = Function(self.__prepared_source, self.__filename())

    _tripleQuotedString = re.compile(
        r"^([ \t]*)[uU]?([rR]?)(('''|\"\"\")(.*)\4)", re.MULTILINE | re.DOTALL)

    def prepareSource(self, source):
        """Prepare source."""
        # compile() don't accept '\r' altogether
        source = source.replace("\r\n", "\n")
        source = source.replace("\r", "\n")
        if isinstance(source, unicode):
            # Use special conversion function to work around
            # compiler-module failure to handle unicode in literals
            try:
                source = source.encode('ascii')
            except UnicodeEncodeError:
                return self._tripleQuotedString.sub(_print_usrc, source)
        return self._tripleQuotedString.sub(r"\1print \2\3", source)


    def getSource(self):
        """Get the original source code."""
        return self.__source

    source = property(getSource, setSource)

    def __call__(self, request, **kw):
        output = StringIO()
        if self._v_compiled is None:
            self._v_compiled = Function(self.__prepared_source,
                                               self.__filename())
        parent = getParent(self)
        kw['request'] = request
        kw['script'] = self
        kw['untrusted_output'] = kw['printed'] = output
        kw['context'] = parent
        kw['script_result'] = None
        if IScriptContainer.providedBy(parent):
            parent.updateGlobals(kw)
        self._v_compiled(kw)
        result = kw['script_result']
        if result == output:
            result = result.getvalue().decode('unicode-escape')
        return result


class Function(object):
    """A compiled function.
    """

    def __init__(self, source, filename='<string>'):
        lines = []
        lines.insert(0, 'def dummy(): \n    pass')
        for line in source.splitlines():
            lines.append('    ' + line)
        lines.append('script_result = dummy()')
        source = '\n'.join(lines)
        #print source
        self.code = compile(source, filename, 'exec')

    def __call__(self, globals):
        globals['__builtins__'] = SafeBuiltins
        exec self.code in globals, None


def _print_usrc(match):
    string = match.group(3)
    raw = match.group(2)
    if raw:
        return match.group(1)+'print '+`string`
    return match.group(1)+'print '+match.group(3).encode('unicode-escape')