===============================
Zope 3 extensions using Twisted
===============================

$Id$

manhole
=======

A simple twisted manhole that allows you to access a running Zope 3
instance via a python command line without having to run ZEO.

You may start it for testing purposes via `python manhole.py` (note that
the twisted library must be reachable via your PYTHONPATH) and log in
from another console window using `ssh -p 5001 admin@localhost`. The
password is defined in the "reactor.listenTCP()" statement of the
manhole.py script.

Note that this will open up a serious security hole on your computer
as now anybody knowing this password may login from remote to the Python
console and get full access to the system with the permissions of the user
running the manhole script.

The script may be stopped with Ctrl-C.

In order to use it with Zope copy the cybertools.twisted-configure.zcml
to the etc/package-includes directory of your Zope instance and restart
Zope. You can then log in with ssh like shown above, using the username
and password of the zope.manager principal defined in your principals.zcml.

After logging in use the `help` command to get more information.

Dependencies
------------

Zope 3.2+ with Twisted as server component

PyOpenSSL: http://pyopenssl.sourceforge.net

PyCrypto: http://www.amk.ca/python/code/crypto.html

Installation
------------

Create a directory `cybertools` somewhere in your Python path, typically
in lib/python of your Zope instance, and put an empty __init__.py there.

In this directory, check out the the cybertools.twisted package:

    svn co svn://svn.cy55.de/Zope3/src/cybertools/trunk/twisted

In order to use it with Zope copy the cybertools.twisted-configure.zcml
to the etc/package-includes directory of your Zope instance and restart
Zope.

Acknowledgements
================

Thanks to Abe Fettig who provides a good introduction to Twisted and some
of the code used for this package with his book
"Twisted Network Programming Essentials".

