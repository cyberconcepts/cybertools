# cybertools.catalog.keyword

"""Keyword catalog index.
"""

import zope.index.keyword
import zope.interface

import zope.app.container.contained
import zope.catalog.attribute
import zope.catalog.interfaces


class IKeywordIndex(zope.catalog.interfaces.IAttributeIndex,
                    zope.catalog.interfaces.ICatalogIndex):
    """Interface-based catalog keyword index.
    """


@zope.interface.implementer(IKeywordIndex)
class KeywordIndex(zope.catalog.attribute.AttributeIndex,
                 zope.index.keyword.KeywordIndex,
                 zope.app.container.contained.Contained):

    pass
