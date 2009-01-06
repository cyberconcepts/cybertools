==============================
Yet Another WikiWiki Framework
==============================

  ($Id$)


An Example for an Elementary Wiki Structure
===========================================

  >>> from cybertools.wiki.base.wiki import WikiManager, Wiki

We create a wiki manager with one wiki that in turn contains a simple
start page.

  >>> manager = WikiManager()
  >>> wiki = manager.addWiki(Wiki('demo_wiki'))
  >>> startPage = wiki.createPage('start_page')

We format the content of the start page using the restructured text format.

  >>> startPage.text = '''
  ... **Welcome to the Demo Wiki**
  ... '''

The parser for restructured text and a corresponding HTML writer are the
default plugins used, so we can already render the page as HTML.

  >>> tree = startPage.parse()

  >>> print startPage.render()
  <p><strong>Welcome to the Demo Wiki</strong></p>


A Very Basic Wiki Format
========================

(this is probably obsolete, will be replaced by corresponding WikiPage
parsing and rendering functionality)

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
