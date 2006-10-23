====================================
User tracking in the loops framework
====================================

  ($Id$)

  >>> from cybertools.tracking.btree import TrackingStorage

  >>> tracks = TrackingStorage()
  >>> runId = tracks.startRun('a001')
  >>> tracks.saveUserTrack('a001', runId, 'u1', {'somekey': 'somevalue'})
  '0000001'
  >>> t1 = tracks.getUserTrack('a001', runId, 'u1')
  >>> t1.data
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

The tracks of a tracking store may be reindexed:

  >>> tracks.reindexTracks()


Fin de partie
=============

