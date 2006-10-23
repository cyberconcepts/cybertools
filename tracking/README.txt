====================================
User tracking in the loops framework
====================================

  ($Id$)

  >>> from cybertools.tracking.btree import TrackingStorage

  >>> tracks = TrackingStorage()
  >>> tracks.saveUserTrack('a001', 0, 'u1', {'somekey': 'somevalue'})
  '0000001'
  >>> t1 = tracks.getUserTracks('a001', 0, 'u1')
  >>> len(t1)
  1
  >>> t1[0].data
  {'somekey': 'somevalue'}
  >>> tracks.getUserNames('a001')
  ['u1']
  >>> tracks.getUserNames('a002')
  []
  >>> [str(id) for id in tracks.getTaskIds()]
  ['a001']

  >>> tracks.query(taskId='a001')
  [<Track ['a001', 1, 'u1', '...-...-... ...:...']: {'somekey': 'somevalue'}>]

  >>> tracks.saveUserTrack('a002', 0, 'u1', {'somekey': 'anothervalue'})
  '0000002'
  >>> result = tracks.query(userName='u1')
  >>> len(result)
  2

What happens if we store more than on record for one set of keys?

  >>> tracks.saveUserTrack('a001', 0, 'u1', {'somekey': 'newvalue'})
  '0000003'
  >>> t2 = tracks.getUserTracks('a001', 0, 'u1')
  >>> [t.data for t in t2]
  [{'somekey': 'somevalue'}, {'somekey': 'newvalue'}]

The tracks of a tracking store may be reindexed:

  >>> tracks.reindexTracks()


Fin de partie
=============

