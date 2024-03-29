#
#  Copyright (c) 2013 Helmut Merz helmutm@cy55.de
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
Date and time utilities.
"""

import time
from datetime import datetime
try:
    import pytz
except ImportError:
    pytz = None


def getTimeStamp():
    return int(time.time())

def date2TimeStamp(d):
    if isinstance(d, (int, float)):
        return int(d)
    return int(time.mktime(d.timetuple()))


def timeStamp2Date(ts, useGM=False):
    if ts is None:
        ts = getTimeStamp()
    if not isinstance(ts, (int, float)): # seems to be a date already
        return ts
    return datetime.fromtimestamp(ts)

def timeStamp2ISO(ts, useGM=False, format='%Y-%m-%d %H:%M'):
    return formatTimeStamp(ts, useGM, format)

def formatTimeStamp(ts, useGM=False, format='%Y-%m-%d %H:%M'):
    if ts is None:
        ts = getTimeStamp()
    fct = useGM and time.gmtime or time.localtime
    return time.strftime(format, fct(ts))


def str2timeStamp(s):
    s = s.replace('T', ' ')
    try:
        t = time.strptime(s[:19], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            t = time.strptime(s[:16], '%Y-%m-%d %H:%M')
        except ValueError:
            t = time.strptime(s[:10], '%Y-%m-%d')
    return int(time.mktime(t))


def strptime(s, format='%Y-%m-%d %H:%M:%S'):
    return datetime(*(time.strptime(s, format)[:6]))


def year(d=None):
    if d is None:
        d = datetime.today()
    return d.year

def toLocalTime(d):
    if pytz is None or not d:
        return d
    cet = pytz.timezone('CET')
    try:
        if not isinstance(d, datetime):
            d = datetime(d.year, d.month, d.day)
        return d.astimezone(cet)
    except ValueError:
        return d

def month(d=None):
    if d is None:
        d = datetime.today()
    return d.month

def day(d=None):
    if d is None:
        d = datetime.today()
    return d.day
