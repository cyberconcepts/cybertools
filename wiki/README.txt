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
  <p><strong>Welcome to the Demo Wiki</strong></p>

We now create another page that contains a link to the start page.

  >>> aboutPage = wiki.createPage('about')
  >>> aboutPage.text = '''
  ... **Information about the Demo Wiki**
  ...
  ... This is the cybertools demo wiki.
  ...
  ... `Back to the Start Page <start_page>`_
  ... '''

  >>> print aboutPage.render()
  processing reference:
    <reference name="Back to the Start Page"
               refuri="start_page">Back to the Start Page</reference>
  <p><strong>Information about the Demo Wiki</strong></p>
  <p>This is the cybertools demo wiki.</p>
  <p><a class="reference" href="start_page">Back to the Start Page</a></p>

