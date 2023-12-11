# cybertools.tracking.migration

"""Tools for migration ZODB-/BTree-based tracks to SQL-base records."""

from cco.storage.tracking import record


def migrate(loopsRoot, recFolderName, storageFactory=record.Storage):
    rf = loopsRoot.getRecordManager().get(recFolderName)
    if rf is None:
        print('*** ERROR: folder %r not found!' % recFolderName)
        return
    for id, inTrack in rf.items():
        print('***', id, inTrack)

