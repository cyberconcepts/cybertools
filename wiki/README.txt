==============================
Yet Another WikiWiki Framework
==============================

  ($Id$)


Links and Link Management
=========================

  >>> from cybertools.wiki.base import link

  >>> manager = link.LinkManager()

  >>> input = ('This is text with a [[wikilink Wiki Link]] and a '
  ...          '`RestructuredText Link <rstxlink>`__')

  >>> page = object()
  >>> format = link.DoubleBracketLinkFormat(page)
  >>> format.manager = manager

  >>> format.unmarshall(input)
  'This is text with a [[##0000001##]] and a `RestructuredText Link <rstxlink>`__'

  >>> link = manager.links['0000001']

  >>> link.original
  '[[wikilink Wiki Link]]'

  >>> link.target
  'wikilink'

  >>> link.label
  'Wiki Link'

