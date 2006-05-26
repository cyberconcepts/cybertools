Knowledge management, learning, and similar stuff
=================================================

  ($Id$)

Let's first set up a tree of knowledge elements (topics) and their
interdependencies:

  >>> from cybertools.knowledge.element import KnowledgeElement
  >>> progLang = KnowledgeElement()
  >>> ooProg = KnowledgeElement()
  >>> python = KnowledgeElement()
  >>> pyBasics = KnowledgeElement()
  >>> pyOo = KnowledgeElement()
  >>> pySpecials = KnowledgeElement()

The knowledge may be organized in a hierarchy (taxonomy) of topics; we
don't use this at the moment but it is important to give the knowledge
an overall structure.

  >>> python.parent = progLang
  >>> pyBasics.parent = python
  >>> pyOo.parent = python
  >>> pySpecials.parent = python

An important point here is that a knowledge element may depend on another;
this means that somebody first has to acquire one of the knowledge elements
before being able to acquire a dependent element. In our example one
would first have to study object-oriented programming in general and the
Python basics before being able to study object oriented programming
with Python.

  >>> pyOo.dependsOn(ooProg)
  >>> pyOo.dependsOn(pyBasics)

Now we create a person that knows about basic Python programming:

  >>> from cybertools.knowledge.knowing import Knowing
  >>> john = Knowing()
  >>> john.knows(pyBasics)

Next we have a requirement profile for knowledge in object-oriented
programming with Python:

  >>> from cybertools.knowledge.requirement import RequirementProfile
  >>> req01 = RequirementProfile()
  >>> req01.requires(pyOo)

Now we can ask what knowledge john is lacking if he would like to take
a position with the requirement profile:

  >>> missing = john.getMissingKnowledge(req01)
  >>> missing
  (<...KnowledgeElement...>, <...KnowledgeElement...>)
  
  >>> missing == (ooProg, pyOo,)
  True  

Luckily there are a few elearning content objects out there that
provide some of the knowledge needed:

  >>> from cybertools.knowledge.provider import KnowledgeProvider
  >>> doc01 = KnowledgeProvider()
  >>> doc02 = KnowledgeProvider()

  >>> doc01.provides(ooProg)
  >>> doc02.provides(pyOo)

So that we are now able to find out what john has to study in order to
fulfill the position offered:

  >>> prov = list(john.getProvidersNeeded(req01))
  >>> len(prov)
  2
  >>> [d[0] for k, d in prov] == [doc01, doc02]
  True
  
