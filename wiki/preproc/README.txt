============================
Standard Wiki Pre-processors
============================

  ($Id$)


MediaWiki Links
===============

  >>> from cybertools.wiki.preproc.mediawiki import preprocess

  >>> src = '''Some text with [[a link]] and
  ... [[link2 | another link]] with separate text.'''

  >>> preprocess(src)
  'Some text with `a link <a link>`__ and\n`another link <link2>`__ with separate text.'
