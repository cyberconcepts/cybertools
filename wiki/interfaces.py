#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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
Interfaces for Wiki functionality.

$Id$
"""

from zope.interface import Interface, Attribute


class IWikiConfiguration(Interface):
    """ Provides information about the implementations to be used for
        the various kinds of wiki plug-ins.
    """

    writer = Attribute('Plug-in component converting from internal tree '
                'format to presentation format.')
    parser = Attribute('Plug-in component converting from text input '
                'format to internal tree format.')

    def getConfigParent():
        """ Return the parent object in case this configuration does not
            provide configuration information for a certain functionality.
        """

    def getConfig(functionality):
        """ Return the name of the plugin that should used for the
            functionality given.
        """


class IWikiManager(Interface):
    """ Manages wikis and wiki-related objects, like plugins.
    """

    def addWiki(wiki):
        """ Register the wiki given.
        """

    def removeWiki(wiki):
        """ Remove the wiki given from the list of wikis.
        """

    def listWikis():
        """ Return a collection of wikis managed by this object.
        """

    def getPlugin(type, name):
        """ Return the plugin of the type given with the name given.
        """

    def getUid(obj):
        """ Return the unique id of the object given.
        """

    def getObject(uid):
        """ Return the object referenced by the unique id given.
        """

class IWiki(Interface):
    """ A collection of wiki pages, or - more generally - wiki components.
    """

    name = Attribute('The name or address of the wiki unique within the '
                'scope of the wiki manager.')
    pages = Attribute('')

    def getManager():
        """ Return the wiki manager this wiki is managed by.
        """

    def createPage(name, title=None):
        """ Create a new wiki page identified by the name (address -
            may be a path) given and return it.
        """

    def removePage(name):
        """ Remove the page identified by name from the wiki, cleaning up
            all information related to the page.
        """

    def getPage(name):
        """ Return the page with the name given or None if not present.
        """

    def listPages():
        """ Return a collection of the pages belonging to this wiki.
        """


class IWikiPage(Interface):
    """ An object representing a page of a wiki.
    """

    name = Attribute('A page name or address unique within the wiki.')
    title = Attribute('A short string describing the wiki page the may be '
                'use as a page title.')
    text = Attribute('The page content in input text format.')

    def getWiki():
        """ The wiki this page belongs to.'
        """

    def render(request=None):
        """ Convert the source text of the page to presentation format.
        """

    def parse(source):
        """ Convert the source text of the page to a document tree.
        """

    def write(tree):
        """ Convert the document tree given to presentation format.
        """

    def preprocess(source):
        """ Modify the source text of the page before parsing it and return it.
        """

    def postprocess(result):
        """ Modify the output of the write process and return it.
        """


# wiki plugins

class IParser(Interface):
    """ Converts from (plain text) input format to internal tree format.
    """

    def parse(text, context=None, request=None):
        """ Return internal tree structure.
        """

class IWriter(Interface):
    """ Converts from internal tree format to presentation format.
    """

    def write(tree):
        """ Returns presentation format for the tree given.
        """


class INodeProcessor(Interface):
    """ Processes a document tree.
    """

    context = Attribute('The node to be processed.')
    parent = Attribute('The parent (=tree) processor.')

    def process():
        """ Do what is necessary.
        """

    def getProperties():
        """ Return a dictionary of properties provided by the context
            node that may be needed for processing.
        """


# wiki elements

class ILinkManager(Interface):
    """ Manages (and possibly contains) all kinds of wiki-related links.
    """

    def createLink(name, source, target, **kw):
        """ Create, register, and return a link record.

            Optional attributes are given as keyword arguments.
        """

    def removeLink(link):
        """ Remove a link.
        """

    def getLink(identifier):
        """ Return the link record identfied by the identifier given or None if
            not present.
        """

    def query(source=None, target=None, name=None, **kw):
        """ Search for link records matching the criteria given. One of
            source or target must be given, the other one and name are optional.

            Additional (optional) criteria may be supported by the implementation.
        """


class ILink(Interface):
    """ A hyperlink between two local or foreign objects.

        There may be more than one link records with the same name
        that represent the real link at different times or under
        different conditions.
    """

    identifier = Attribute('An internal identifier of the link record, '
                'unique within the link manager.')
    name = Attribute('The external identifier for the link, i.e. the '
                'string used in the source text to address the link.')
    title = Attribute('A short text, may be used as the default text for '
                'the link or for the alt tag of an image. Could also serve '
                'for identifying a new link.')
    description = Attribute('Optional: some text, may be used as a title attribute.')
    state = Attribute('A short string denoting the state of the link entry.')
    source = Attribute('Identifier of the link\'s source object.')
    target = Attribute('Identifier of the link\'s target object or - '
        'for external links - the target URI.')
    targetFragment = Attribute('Optional: an address part leading to a '
                'text anchor or the part of an image.')
    refuri = Attribute('The URI linking to the target object.')
    user = Attribute('Optional: a string denoting the creator of the record.')
    run = Attribute('Optional: May be used to group the links from a certain '
                'source at different times.')

    def getManager():
        """ Return the link manager this link is managed by.
        """


class ILinkProcessor(INodeProcessor):
    """ A node processor specialized on links (references).
    """

    source = Attribute('The object from which the link originates, '
                'typically a wiki page.')
    request = Attribute('Optional request or environment object, necessary '
                'e.g. for rendering an URI.')
    targetName = Attribute('The name used for addressing the link target object.')

    def setUri(uri):
        """ Record the real reference URI to be used for the link on the
            rendered page.
        """

    def markPresentation(feature):
        """ Record a presentation feature for the link on the rendered page,
            for HTML rendering this would be a class name.
        """

    def addText(text):
        """ Add additional text to the link on the rendered page.
        """
