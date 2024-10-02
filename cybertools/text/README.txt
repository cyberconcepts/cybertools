=================================================
Text Transformations, e.g. for Full-text Indexing
=================================================

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
  >>> f = open(os.path.join(testdir, 'selfhtml.html'), encoding='ISO8859-15')
  >>> html = f.read()
  >>> text = htmlToText(html)
  >>> '<p>' in html
  True
  >>> '<p>' in text
  False
  >>> f.close()

PDF Files
---------

Let's start with a PDF file:

  >>> from cybertools.text.pdf import PdfTransform
  >>> transform = PdfTransform(None)
  >>> f = open(os.path.join(testdir, 'mary.pdf'), 'rb')

This will be transformed to plain text:

  >>> result = transform(f)

Let's check the log, should be empty:

  >>> print(log)

So what is in the plain text result?

  >>> words = result.split()
  >>> len(words)
  89
  >>> u'lamb' in words
  True
  >>> f.close()

Word Documents
--------------

  >>> from cybertools.text.doc import DocTransform
  >>> transform = DocTransform(None)
  >>> f = open(os.path.join(testdir, 'mary.doc'), 'rb')
  >>> result = transform(f)
  >>> print(log)
  >>> words = result.split()
  >>> len(words)
  89
  >>> u'lamb' in words
  True
  >>> f.close()

RTF Files
---------

  >>> from cybertools.text.rtf import RtfTransform
  >>> transform = RtfTransform(None)
  >>> f = open(os.path.join(testdir, 'mary.rtf'), 'rb')
  >>> result = transform(f)
  >>> print(log)
  zope.server WARNING
    rtf2xml is not available

>> words = result.split()
>> len(words)
90
>> u'lamb' in words
True

  >>> f.close()

PowerPoint Presentations
------------------------

  >>> from cybertools.text.ppt import PptTransform
  >>> transform = PptTransform(None)
  >>> f = open(os.path.join(testdir, 'mary.ppt'), 'rb')
  >>> result = transform(f)
  >>> print(log)
  zope.server WARNING
    rtf2xml is not available
  zope.server WARNING
    ppthtml is not available

>> words = result.split()
>> len(words)
102
>> u'lamb' in words
True

  >>> f.close()

Excel Spreadsheets
------------------

  >>> from cybertools.text.xls import XlsTransform
  >>> transform = XlsTransform(None)
  >>> f = open(os.path.join(testdir, 'mary.xls'), 'rb')
  >>> result = transform(f)
  >>> words = result.split()
  >>> len(words)
  89
  >>> u'lamb' in words
  True
  >>> f.close()

OpenOffice
----------

  >>> from cybertools.text.ooffice import OOTransform
  >>> transform = OOTransform(None)
  >>> f = open(os.path.join(testdir, 'mary.odt'), 'rb')
  >>> result = transform(f)
  >>> len(words)
  89
  >>> u'lamb' in words
  True
  >>> f.close()

  >>> f = open(os.path.join(testdir, 'mary.ods'), 'rb')
  >>> result = transform(f)
  >>> len(result.split())
  89
  >>> f.close()

  >>> f = open(os.path.join(testdir, 'mary.odp'), 'rb')
  >>> result = transform(f)
  >>> len(result.split())
  99
  >>> f.close()
