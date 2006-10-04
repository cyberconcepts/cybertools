=================================================
Text transformations, e.g. for full-text indexing
=================================================

  ($Id$)

  >>> import os
  >>> from cybertools import text
  >>> directory = os.path.dirname(text.__file__)
  >>> fn = os.path.sep.join((directory, 'testfiles', 'mary.pdf'))
  >>> f = open(fn)

  >>> from cybertools.text.pdf import PdfTransform
  >>> transform = PdfTransform(None)
  >>> words = transform(f).split()
  >>> len(words)
  89
  >>> u'lamb' in words
  True
