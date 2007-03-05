=================================================
Text Transformations, e.g. for Full-text Indexing
=================================================

  ($Id$)

If a converter program needed is not available we want to put a warning
into Zope's server log; in order to be able to test this we register
a log handler for testing:

  >>> from zope.testing.loggingsupport import InstalledHandler
  >>> log = InstalledHandler('zope.server')

The test files are in a subdirectory of the text package:

  >>> import os
  >>> from cybertools import text
  >>> testdir = os.path.join(os.path.dirname(text.__file__), 'testfiles')

HTML
----

  >>> from cybertools.text.html import htmlToText
  >>> html = open(os.path.join(testdir, 'selfhtml.html')).read()
  >>> text = htmlToText(html)
  >>> '<p>' in html
  True
  >>> '<p>' in text
  False

PDF Files
---------

Let's start with a PDF file:

  >>> from cybertools.text.pdf import PdfTransform
  >>> transform = PdfTransform(None)
  >>> f = open(os.path.join(testdir, 'mary.pdf'))

This will be transformed to plain text:

  >>> result = transform(f)

Let's check the log, should be empty:

  >>> print log

So what is in the plain text result?

  >>> words = result.split()
  >>> len(words)
  89
  >>> u'lamb' in words
  True

Word Documents
--------------

  >>> from cybertools.text.doc import DocTransform
  >>> transform = DocTransform(None)
  >>> f = open(os.path.join(testdir, 'mary.doc'))
  >>> result = transform(f)
  >>> print log
  >>> words = result.split()
  >>> len(words)
  89
  >>> u'lamb' in words
  True
