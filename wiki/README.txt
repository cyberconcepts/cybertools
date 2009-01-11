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

  >>> print startPage.render()
  visiting document
  visiting paragraph
  visiting strong
  visiting #text
  <p><strong>Welcome to the Demo Wiki</strong></p>


