XML (and XHTML) Generation
==========================

The elements generator lets you easily create snippets of XML or XHTML:

  >>> from cybertools.xml.element import elements as e
  >>> doc = e.html(
  ...     e.head(e.title(u'Page Title')),
  ...     e.body(
  ...       e.div(u'The top bar', class_=u'top'),
  ...       e.div(u'The body stuff', class_=u'body'),
  ... ))

  >>> print doc.render()
  <html>
    <head>
      <title>
        Page Title
      </title>
    </head>
    <body>
      <div class="top">
        The top bar
      </div>
      <div class="body">
        The body stuff
      </div>
    </body>
  </html>

An XML element thus created may be converted to an ElementTree (the standard
implementation in fact uses an lxml.etree structure as its basis):

  >>> doc.renderTree()
  '<html><head><title>Page Title</title></head><body><div class="top">The top bar</div><div class="body">The body stuff</div></body></html>'

  >>> tree = doc.makeTree()
  >>> tree.findtext('head/title')
  'Page Title'

  >>> xml = ('<html><head><title>Page Title</title></head><body>'
  ... '<div class="top">The top bar</div>'
  ... '<div class="body">The body stuff</div></body></html>')
  >>> from cybertools.xml.element import fromXML
  >>> doc = fromXML(xml)
  >>> print doc.render()
  <html>
    <head>
      <title>
        Page Title
      </title>
    </head>
    <body>
      <div class="top">
        The top bar
      </div>
      <div class="body">
        The body stuff
      </div>
    </body>
  </html>

Alternative Notation
--------------------

We can also create such a structure by successively adding elements
just by accessing an element's attributes:

  >>> doc = e.html
  >>> dummy = doc.head.title(u'Page Title')
  >>> body = doc.body
  >>> div1 = body.div(u'The top bar', class_=u'top')
  >>> div2 = body.div(u'The body stuff', class_=u'body')
  >>> print doc.render()
  <html>
    <head>
      <title>
        Page Title
      </title>
    </head>
    <body>
      <div class="top">
        The top bar
      </div>
      <div class="body">
        The body stuff
      </div>
    </body>
  </html>

  >>> for text in (u'Welcome', u'home'):
  ...     p = div2.p(text, style='font-size: 80%;')
  >>> print doc.render()
  <html>...<p...>...</p>...

  >>> x = p('Some more text').b('bold text')
  >>> x = p('and normal again')
  >>> print p.render()
  <p...>...home...Some more text
    <b>...bold text...</b>
    ...and normal again
  </p>

