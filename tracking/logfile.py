#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Track user interactions by writing to a log file, loading the log at
certain times collecting analysis results in a real tracking storage.

$Id$
"""

import logging
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
