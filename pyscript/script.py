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

""" Simple implementation of Python scripts.

$Id$
"""

import new
import re
import compiler.pycodegen
from cStringIO import StringIO
from persistent import Persistent
import RestrictedPython.RCompile
from RestrictedPython.SelectCompiler import ast
from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import Contained
from zope.interface import implements
from zope.proxy import removeAllProxies
from zope.security.untrustedpython.builtins import SafeBuiltins
from zope.security.untrustedpython.rcompile import RestrictionMutator as BaseRM
from zope.traversing.api import getParent, getPath

from cybertools.pyscript.interfaces import IPythonScript, IScriptContainer
try:
    #from cybertools.pyscript.rstat import r, rpy
    import rpy
    from rpy import r
    HAS_R = True
except ImportError:
    HAS_R = False


unrestricted_objects = ('rpy', 'r', 'as_py', 'rstat')


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

    title = u''
    parameters = u''
    source = u''
    contentType=u'text/plain'

    def __init__(self, title=u'', parameters=u'', source=u'',
                 contentType=u'text/plain'):
        """Initialize the object."""
        super(PythonScript, self).__init__()
        self.title = title
        self.source = source
        self.contentType = contentType
        self.parameters = parameters or u''

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
        self._v_compiled = Function(self.__prepared_source,  self.parameters,
                                    self.__filename())

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

    def __call__(self, request, *args, **kw):
        output = StringIO()
        if self._v_compiled is None:
            self._v_compiled = Function(self.__prepared_source, self.parameters,
                                        self.__filename(),)
        parent = getParent(self)
        kw['request'] = request
        kw['script'] = self
        kw['untrusted_output'] = kw['printed'] = output
        kw['context'] = parent
        kw['script_result'] = None
        if IScriptContainer.providedBy(parent):
            parent.updateGlobals(kw)
        self._v_compiled(args, kw)
        result = kw['script_result']
        if result == output:
            result = result.getvalue().decode('unicode-escape')
        return result


class Function(object):
    """A compiled function.
    """

    parameters = []

    def __init__(self, source, parameters='', filename='<string>'):
        lines = []
        if parameters:
            self.parameters = [str(p).strip() for p in parameters.split(',')]
        #print '*** Function.parameters:', repr(self.parameters)
        lines.insert(0, 'def dummy(): \n    pass')
        for line in source.splitlines():
            lines.append('    ' + line)
        lines.append('script_result = dummy()')
        source = '\n'.join(lines)
        #print '*** source:', source
        self.code = compile(source, filename, 'exec')

    def __call__(self, args, globals):
        globals['__builtins__'] = SafeBuiltins
        for idx, p in enumerate(self.parameters):
            # TODO: handle parameters with default values like ``attr=abc``
            globals[p] = args[idx]
        exec self.code in globals, None


def _print_usrc(match):
    string = match.group(3)
    raw = match.group(2)
    if raw:
        return match.group(1)+'print '+`string`
    return match.group(1)+'print '+match.group(3).encode('unicode-escape')


class ScriptContainer(BTreeContainer):

    implements(IScriptContainer)

    unrestricted_objects = ('rstat',)  # not used (yet)

    def getItems(self):
        return self.values()

    def updateGlobals(self, globs):
        if HAS_R:
            from cybertools.pyscript import rstat
            context = globs['context']
            request = globs['request']
            globs['rstat'] = rstat.RStat(context, request)
            globs['r'] = r
            globs['rpy'] = rpy

