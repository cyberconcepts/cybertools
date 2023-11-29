=============
Notifications
=============

  ($Id$)

  >>> from zope import component
  >>> from cybertools.tracking.btree import TrackingStorage
  >>> from cybertools.tracking.notify.base import Notification, NotificationManager
  >>> component.provideAdapter(NotificationManager)

  >>> notifications = TrackingStorage(trackFactory=Notification)

  >>> from cybertools.tracking.notify.interfaces import INotificationManager
  >>> manager = INotificationManager(notifications)


Storing and Retrieving Notifications
====================================

  >>> manager.notify('obj01', 'user01', 'object_changed')

  >>> ntf01 = list(manager.query(userName='user01'))[0]
  >>> ntf01
  <Notification ['obj01', 1, 'user01', '...']:
  {'type': 'object_changed', 'state': 'new', 'media': ['inbox']}>

  >>> print(ntf01.state)
  new
  >>> print(ntf01.timingType)
  None
