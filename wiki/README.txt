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
to make sure the correct link manager will be used.

  >>> manager = WikiManager()

  >>> linkManagerName = 'cybertools.link'
  >>> manager.setConfig('linkManager', linkManagerName)
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

  >>> from cybertools.link.interfaces import ILinkManager
  >>> linkManager = manager.getPlugin(ILinkManager, linkManagerName)
  >>> links = linkManager.links
  >>> len(links)
  1
  >>> link = links.values()[0]
  >>> link.source, link.target, link.name
  (0, 1, u'start_page')

Links to not yet existing pages
-------------------------------

When a referenced page does not exist yet a special link is created that
should lead to a view that will create the page.

  >>> aboutPage.text += '''
  ... `More... <more>`_
  ... '''
  >>> print aboutPage.render(TestRequest())
  <p><strong>Information about the Demo Wiki</strong></p>
  <p>This is the cybertools demo wiki.</p>
  <p><a class="reference"
        href="http://127.0.0.1/demo_wiki/start_page">Back to the Start Page</a></p>
  <p><a class="reference create"
        href="http://127.0.0.1/demo_wiki/&#64;&#64;create.html?name=more">?More...</a></p>

Again a link object has been created that will be reused for subsequent
rendering operations.

  >>> len(links)
  2

  >>> print aboutPage.render(TestRequest())
  <p>...
  <p><a class="reference create"
        href="http://127.0.0.1/demo_wiki/&#64;&#64;create.html?name=more">?More...</a></p>
  >>> len(links)
  2

Links with fragments (anchor references) and parameters
-------------------------------------------------------

  >>> referencePage = wiki.createPage('reference')
  >>> referencePage.text = '''
  ... References
  ... ==========
  ...
  ... - `About content <about#content?language=en>`_
  ... - `More content <more#content?language=en>`_
  ... '''

  >>> print referencePage.render(TestRequest())
  <h1 class="title">References</h1>
  <ul class="simple">
  <li><a class="reference"
         href="http://127.0.0.1/demo_wiki/about#content?language=en">About content</a></li>
  <li><a class="reference create"
         href="http://127.0.0.1/demo_wiki/&#64;&#64;create.html?name=more#content?language=en">?More content</a></li>
  </ul>

External links
--------------

  >>> linksPage = wiki.createPage('links')
  >>> linksPage.text = '''
  ... **A collection of interesting links**
  ...
  ... - http://python.org#library
  ... - `Zope <http://zope.org?lang=de>`_
  ... '''

An absolute URL given as link target will not be changed in the process.

  >>> print linksPage.render(TestRequest())
  <p><strong>A collection of interesting links</strong></p>
  <ul class="simple">
  <li><a class="reference"
         href="http://python.org#library">http://python.org#library</a></li>
  <li><a class="reference" href="http://zope.org?lang=de">Zope</a></li>
  </ul>

Nevertheless the links are registered in the link manager.

  >>> len(links)
  6

When we render external links repeatedly no new link objects will be
created.

  >>> print linksPage.render(TestRequest())
  <p><strong>A collection of interesting links</strong></p>
  <ul class="simple">
  <li><a class="reference"
         href="http://python.org#library">http://python.org#library</a></li>
  <li><a class="reference" href="http://zope.org?lang=de">Zope</a></li>
  </ul>

  >>> len(links)
  6


Media Objects
=============

