# cybertools.tracking.logfile

""" Track user interactions by writing to a log file, loading the log at
certain times collecting analysis results in a real tracking storage.
"""

import logging
import logging.handlers
import os


class Logger(object):

    handler = None

    def __init__(self, logname, logfile,
                 logformat='%(asctime)s;%(message)s', **kw):
        self.logname = logname
        self.logfile = logfile
        self.logformat = logformat
        self.params = kw
        self.setup()

    def setup(self):
        directory = os.path.dirname(self.logfile)
        if not os.path.exists(directory):
            os.makedirs(directory)
        logger = logging.getLogger(self.logname)
        self.handler = logging.handlers.RotatingFileHandler(self.logfile,
                            backupCount=self.params.get('backupCount', 5),
                            encoding='UTF-8')
        formatter = logging.Formatter(self.logformat)
        self.handler.setFormatter(formatter)
        if not logger.handlers:
            logger.addHandler(self.handler)
        logger.setLevel(logging.INFO)

    def log(self, message):
        logging.getLogger(self.logname).info(message)

    def doRollover(self):
        if self.handler is not None:
            self.handler.doRollover()


loggers = {}
