==============
Python Scripts
==============

Persistent Python Scripts

Examples:

  >>> from cybertools.pyscript.tests import Root
  >>> from cybertools.pyscript.script import PythonScript

  >>> pp = PythonScript()
  >>> pp.__parent__ = Root()
  >>> pp.__name__ = 'pp'
  >>> request = None

Test that can produce the correct filename

  >>> pp._PythonScript__filename()
  u'/pp'

A simple test that checks that any lone-standing triple-quotes are
being printed.

  >>> pp.setSource(u"'''<html>...</html>'''\nreturn printed")
  >>> pp(request)
  u'<html>...</html>\n'

Make sure that strings with prefixes work.

  >>> pp.setSource(ur"ur'''test\\r'''" + "\nreturn printed")
  >>> pp(request)
  u'test\\r\n'

Make sure that Windows (\r\n) line ends also work.

  >>> pp.setSource(u"if 1 == 1:\r\n\r\n   '''<html>...</html>'''\nreturn printed")
  >>> pp(request)
  u'<html>...</html>\n'

Make sure that unicode strings work as expected.

  >>> pp.setSource(u"u'''\u0442\u0435\u0441\u0442'''\nreturn printed")
  >>> pp(request)
  u'\u0442\u0435\u0441\u0442\n'

Make sure that multi-line strings work.

  >>> pp.setSource(u"u'''test\ntest\ntest'''\nreturn printed")
  >>> pp(request)
  u'test\n...test\n...test\n'

Here you can see a simple Python command...

  >>> pp.setSource(u"print u'<html>...</html>'\nreturn printed")
  >>> pp(request)
  u'<html>...</html>\n'

... and here a triple quote with some variable replacement.

  >>> pp.setSource(u"'''<html>%s</html>''' %x\nreturn printed")
  >>> pp(request, x='test')
  u'<html>test</html>\n'

Make sure that the context of the page is available.

  >>> pp.setSource(u"'''<html>%s</html>''' %context.__name__\nreturn printed")
  >>> pp(request)
  u'<html>root</html>\n'

Make sure that faulty syntax is interpreted correctly.

Note: We cannot just print the error directly, since there is a
'bug' in the Linux version of Python that does not display the filename
of the source correctly. So we construct an information string by hand.

  >>> def print_err(err):
  ...     print ('%(msg)s, %(filename)s, line %(lineno)i, offset %(offset)i'
  ...           % err.__dict__)
  ...
  >>> try:
  ...     pp.setSource(u"'''<html>...</html>") #'''"
  ... except SyntaxError, err:
  ...     print_err(err)
  EOF while scanning triple-quoted string, /pp, line 4, offset 47

  >>> try:
  ...     pp.setSource(u"prin 'hello'")
  ... except SyntaxError, err:
  ...     print_err(err)
  invalid syntax, /pp, line 3, offset 16
