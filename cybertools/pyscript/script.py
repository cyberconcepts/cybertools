# cybertools.pyscript.script

""" Simple implementation of Python scripts.
"""

import os, re
#import compiler.pycodegen
from io import StringIO
from persistent import Persistent
#import RestrictedPython.RCompile
#from RestrictedPython.SelectCompiler import ast
from zope.container.btree import BTreeContainer
from zope.container.contained import Contained
from zope.interface import implementer
from zope.proxy import removeAllProxies
#from zope.security.untrustedpython.builtins import SafeBuiltins
#from zope.security.untrustedpython.rcompile import RestrictionMutator as BaseRM
from zope.traversing.api import getParent, getPath

from cybertools.pyscript.interfaces import IPythonScript, IScriptContainer

HAS_R = use_R = bool(os.environ.get('USE_RLIBRARY', True))

if use_R:
    try:
        #from cybertools.pyscript.rstat import r, rpy
        import rpy
        from rpy import r
        HAS_R = True
    except ImportError:
        HAS_R = False


unrestricted_objects = ('rpy', 'r', 'as_py', 'rstat')


def compile(text, filename, mode):
    if not isinstance(text, str):
        raise TypeError("Compiled source must be string")
    gen = RExpression(text, str(filename), mode)
    gen.compile()
    return gen.getCode()


#class RExpression(RestrictedPython.RCompile.RestrictedCompileMode):
class RExpression(object):

    #CodeGeneratorClass = compiler.pycodegen.ExpressionCodeGenerator

    def __init__(self, source, filename, mode="eval"):
        self.mode = mode
        RestrictedPython.RCompile.RestrictedCompileMode.__init__(
            self, source, filename)
        self.rm = RestrictionMutator()


#class RestrictionMutator(BaseRM):
class RestrictionMutator(object):

    unrestricted_objects = unrestricted_objects

    def visitGetattr(self, node, walker):
        _getattr_name = ast.Name("getattr")
        node = walker.defaultVisitNode(node)
        if node.expr.name in self.unrestricted_objects:
            return node     # no protection
        return ast.CallFunc(_getattr_name,
                            [node.expr, ast.Const(node.attrname)])


@implementer(IPythonScript)
class PythonScript(Contained, Persistent):
    """Persistent Python Page - Content Type
    """

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
        if isinstance(source, str):
            # Use special conversion function to work around
            # compiler-module failure to handle unicode in literals
            try:
                source = source.encode()
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
        #print('*** Function.parameters:', repr(self.parameters))
        lines.insert(0, 'def dummy(): \n    pass')
        for line in source.splitlines():
            lines.append('    ' + line)
        lines.append('script_result = dummy()')
        source = '\n'.join(lines)
        #print('*** source:', source)
        self.code = compile(source, filename, 'exec')

    def __call__(self, args, globals):
        globals['__builtins__'] = SafeBuiltins
        for idx, p in enumerate(self.parameters):
            # TODO: handle parameters with default values like ``attr=abc``
            globals[p] = args[idx]
        exec(self.code, globals, None)


def _print_usrc(match):
    string = match.group(3)
    raw = match.group(2)
    if raw:
        #return match.group(1)+'print '+`string`
        return match.group(1) + 'print(' + eval('string') + ')'
    return match.group(1) + 'print(' + match.group(3).encode('unicode-escape') + ')'


@implementer(IScriptContainer)
class ScriptContainer(BTreeContainer):

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

