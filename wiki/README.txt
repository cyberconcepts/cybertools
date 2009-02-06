==============================
Yet Another WikiWiki Framework
==============================

  ($Id$)

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest


An Example for an Elementary Wiki Structure
===========================================

  >>> from cybertools.wiki.base.wiki import WikiManager, Wiki

We create a wiki manager with one wiki that in turn contains a simple
start page. We also set the ``linkManager`` configuration option explicitly
to make sure the btree-based tracking link manager will be used.

  >>> manager = WikiManager()

  >>> linkManagerName = 'tracking'
  >>> manager.linkManager = linkManagerName
  >>> wiki = manager.addWiki(Wiki('demo_wiki'))
  >>> startPage = wiki.createPage('start_page')

We format the content of the start page using the restructured text format.

  >>> startPage.text = '''
  ... **Welcome to the Demo Wiki**
  ... '''

The parser for restructured text and a corresponding HTML writer are the
default plugins used, so we can already render the page as HTML.

  >>> print startPage.render(TestRequest())
  <p><strong>Welcome to the Demo Wiki</strong></p>

Links to existing pages
-----------------------

We now create another page that contains a link to the start page.

  >>> aboutPage = wiki.createPage('about')
  >>> aboutPage.text = '''
  ... **Information about the Demo Wiki**
  ...
  ... This is the cybertools demo wiki.
  ...
  ... `Back to the Start Page <start_page>`_
  ... '''

  >>> print aboutPage.render(TestRequest())
  <p><strong>Information about the Demo Wiki</strong></p>
  <p>This is the cybertools demo wiki.</p>
  <p><a class="reference"
        href="http://127.0.0.1/demo_wiki/start_page">Back to the Start Page</a></p>

Let's now have a look at the link manager - it should have recorded the link
from the page content.

  >>> from cybertools.wiki.interfaces import ILinkManager
  >>> linkManager = manager.getPlugin(ILinkManager, linkManagerName)
  >>> links = linkManager.links
  >>> len(links)
  1
  >>> link = links.values()[0]
  >>> link.source, link.target, link.name, link.refuri
  (0, 1, u'start_page', 'http://127.0.0.1/demo_wiki/start_page')

Links to not yet existing pages
-------------------------------

  >>> aboutPage.text += '''
  ... `More... <more>`_
  ... '''
  >>> print aboutPage.render(TestRequest())
  <p><strong>Information about the Demo Wiki</strong></p>
  <p>This is the cybertools demo wiki.</p>
  <p><a class="reference"
        href="http://127.0.0.1/demo_wiki/start_page">Back to the Start Page</a></p>
  <p><a class="reference create"
        href="http://127.0.0.1/demo_wiki/create.html?linkid=0000002">?More...</a></p>


