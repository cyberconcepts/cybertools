# cybertools.tracking.migration

"""Tools for migration ZODB-/BTree-based tracks to SQL-base records."""

from datetime import datetime
import time

import config
from cco.storage.common import Context, getEngine
from cco.storage.tracking import record
from loops.config.base import LoopsOptions


def migrate(loopsRoot, recFolderName, storageFactory=record.Storage):
    rf = loopsRoot.getRecordManager().get(recFolderName)
    if rf is None:
        print('*** ERROR: folder %r not found!' % recFolderName)
        return
    options = LoopsOptions(loopsRoot)
    print('*** database:', config.dbname, config.dbuser, config.dbpassword)
    schema = options('cco.storage.schema') or None
    if schema is not None:
        schema = schema[0]
    print('*** schema:', schema)
    context = Context(getEngine(config.dbengine, config.dbname, 
                                config.dbuser, config.dbpassword, 
                                host=config.dbhost, port=config.dbport), 
                      schema=schema)
    storage = storageFactory(context)
    for id, inTrack in rf.items():
        #ts = time.mktime(inTrack.timeStamp.timetuple())
        ts = datetime.fromtimestamp(inTrack.timeStamp)
        print('*** in:', id, inTrack)
        head = [inTrack.metadata[k] for k in storage.trackFactory.headFields]
        print('*** out:', head, ts)
        track = storage.trackFactory(*head, trackId=int(id), 
                                     timeStamp=ts, data=inTrack.data)
        storage.upsert(track)


