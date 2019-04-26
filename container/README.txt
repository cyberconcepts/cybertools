Ordered Containers
==================

  ($Id$)

Let's add an ordered container and place some objects in it:
      
  >>> from zope.app.container.ordered import OrderedContainer
  >>> c1 = OrderedContainer()
  >>> c1['sub1'] = OrderedContainer()
  >>> c1['sub2'] = OrderedContainer()
  >>> c1['sub3'] = OrderedContainer()
  >>> c1['sub4'] = OrderedContainer()
  >>> c1.keys()
  [u'sub1', u'sub2', u'sub3', u'sub4']
      
A special management view provides methods for moving objects down, up,
to the bottom, and to the top
      
  >>> from cybertools.container.ordered import OrderedContainerView
  >>> from zope.publisher.browser import TestRequest
  >>> view = OrderedContainerView(c1, TestRequest())
  >>> view.move_bottom(('sub3',))
  >>> c1.keys()
  [u'sub1', u'sub2', u'sub4', u'sub3']
  >>> view.move_up(('sub4',), 1)
  >>> c1.keys()
  [u'sub1', u'sub4', u'sub2', u'sub3']
  >>> view.move_top(('sub2',))
  >>> c1.keys()
  [u'sub2', u'sub1', u'sub4', u'sub3']
  >>> view.move_down(('sub2',), 2)
  >>> c1.keys()
  [u'sub1', u'sub4', u'sub2', u'sub3']

