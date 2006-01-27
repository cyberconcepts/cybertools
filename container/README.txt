Ordered Containers
==================

  ($Id$)

Let's add an ordered container and place some objects in it:
      
  >>> from zope.interface import implements
  >>> from zope.app.container.interfaces import IOrderedContainer
  >>> import zope.app.container.ordered
  >>> class OrderedContainer(zope.app.container.ordered.OrderedContainer):
  ...     implements(IOrderedContainer)

  >>> c1 = OrderedContainer()
  >>> c1['sub1'] = OrderedContainer()
  >>> c1['sub2'] = OrderedContainer()
  >>> c1['sub3'] = OrderedContainer()
  >>> c1['sub4'] = OrderedContainer()
  >>> c1.keys()
  ['sub1', 'sub2', 'sub3', 'sub4']
      
A special management view provides methods for moving objects down, up,
to the bottom, and to the top
      
  >>> from cybertools.container.ordered import OrderedContainerView
  >>> from zope.publisher.browser import TestRequest
  >>> view = OrderedContainerView(c1, TestRequest())
  >>> view.move_bottom(('sub3',))
  >>> c1.keys()
  ['sub1', 'sub2', 'sub4', 'sub3']
  >>> view.move_up(('sub4',), 1)
  >>> c1.keys()
  ['sub1', 'sub4', 'sub2', 'sub3']
  >>> view.move_top(('sub2',))
  >>> c1.keys()
  ['sub2', 'sub1', 'sub4', 'sub3']
  >>> view.move_down(('sub2',), 2)
  >>> c1.keys()
  ['sub1', 'sub4', 'sub2', 'sub3']

