=========================================
Integrating objects from external systems
=========================================

Integration of external sources.

  ($Id$)


Getting started
===============

Let's do some basic set up

  >>> from zope import component

  >>> from cybertools.integrator.tests import testDir
  >>> from cybertools.integrator.filesystem import ContainerFactory, FileFactory
  >>> from cybertools.integrator.interfaces import IContainerFactory
  >>> component.provideUtility(ContainerFactory(), name='filesystem')
  >>> component.provideUtility(FileFactory(), name='filesystem')


Accessing Objects in the Filesystem
=======================================

  >>> top = component.getUtility(IContainerFactory, name='filesystem')(testDir)
  >>> sorted(top)
  ['index.html', 'sub']
  >>> len(top)
  2

  >>> sub = top['sub']
  >>> sorted(sub)
  ['demo.tgz', 'index.html', 'loops_logo.png']

  >>> file = sub['demo.tgz']
  >>> file.contentType
  'application/x-tar'
  >>> file.getSize()
  432L

  >>> logo = sub['loops_logo.png']
  >>> logo.contentType
  'image/png'
  >>> logo.getImageSize()
  (145, 42)

  >>> html = top['index.html']
  >>> html.contentType
  'text/html'
  >>> print html.data
  <html>...
      <img src="sub/loops_logo.png" />
      <a href="sub">Subdirectory</a>
      <a href="sub/demo.tgz">Demo</a>...
  </html>...

