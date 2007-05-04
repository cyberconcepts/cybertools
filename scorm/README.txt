===================
A generic SCORM API
===================

  ($Id$)

In order to work with the SCORM API we first need a tracking storage.

  >>> from cybertools.tracking.btree import TrackingStorage
  >>> tracks = TrackingStorage()

We can now create a ScormAPI adapter. Note that this adapter is stateless
as usually a new instance is created upon each request.

  >>> from cybertools.scorm.base import ScormAPI
  >>> api = ScormAPI(tracks, 'a001', 0, 'user1')

The first step is always the initialize() call - though in our case it
does not do anything.

  >>> api.initialize()
  '0'

Then we can set some values.

  >>> rc = api.setValue('cmi.interactions.0.id', 'q007')
  >>> rc = api.setValue('cmi.interactions.0.result', 'correct')
  >>> rc = api.setValue('cmi.comments_from_learner', 'Hello SCORM')
  >>> rc = api.setValue('cmi.interactions.1.id', 'q009')
  >>> rc = api.setValue('cmi.interactions.1.result', 'incorrect')

Depending on the data elements the values entered are kept together in
one track or stored in separate track objects. So there is a separate
track for each interaction and one additional track for all the other elements.

  >>> for t in sorted(tracks.values(), key=lambda x: x.timeStamp):
  ...     print t.data
  {'id': 'q007', 'key_prefix': 'cmi.interactions.0', 'result': 'correct'}
  {'cmi.comments_from_learner': 'Hello SCORM', 'key_prefix': ''}
  {'id': 'q009', 'key_prefix': 'cmi.interactions.1', 'result': 'incorrect'}

Using the getValue() method we can retrieve certain values without having
to care about the storage in different track objects.

  >>> api.getValue('cmi.comments_from_learner')
  ('Hello SCORM', '0')
  >>> api.getValue('cmi.interactions.0.id')
  ('q007', '0')
  >>> api.getValue('cmi.interactions.1.result')
  ('incorrect', '0')

We can also query special elements like _count and _children.

  >>> api.getValue('cmi.objectives._count')
  (0, '0')
  >>> api.getValue('cmi.interactions._count')
  (2, '0')

  >>> api.getValue('cmi.interactions._children')
  (('id', 'type', 'objectives', 'timestamp', 'correct_responses',
    'weighting', 'learner_response', 'result', 'latency', 'description'), '0')
  >>> api.getValue('cmi.objectives.5.score._children')
  (('scaled', 'raw', 'min', 'max'), '0')

