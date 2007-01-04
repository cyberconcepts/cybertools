================
Common Utilities
================

$Id$

This package contains a set of miscellaneous utility modules that
are to small for creating a separate package for them.

As each utility is developed further it may eventually get its own
package some time.

Usually each utility has a <name>.py file with an implementation and a
corresponding <name>.txt file with a description that can be run as a
doctest.

The doctests can be run by issuing

  python cybertools/util/tests.py

in the directory above the cybertools directory or via

  bin/test -vs cybertools.util

from within a Zope 3 instance that contains the cybertools package in
its python path.
