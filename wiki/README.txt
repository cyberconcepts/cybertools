==============================
Yet Another WikiWiki Framework
==============================

  ($Id$)


A Very Basic Wiki Format
========================

We first set up a format (a utility) and create a format instance
from it. The instance needs a wiki page as its context - to simplify
things during testing we just use a bare object.

  >>> from cybertools.wiki.base.format import BasicFormat
  >>> format = BasicFormat()
  >>> page = object()
  >>> instance = format.getInstance(page)

Now we enter some simple text and request the format instance to
unmarshall it, i.e. to convert it from the editable to the internal
representation.

  >>> input = ('This is text with a [[Wiki Link]].\n\n'
  ...          'It also contains a second line.')

  >>> instance.unmarshall(input)
  'This is text with a [[${l0000001}]].\n\nIt also contains a second line.'
