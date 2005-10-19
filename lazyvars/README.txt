Setting up and using LazyVars objects
=====================================

Lazy variables are only calculated when really needed, and they are
calculated only once during the lifetime of the LazyVars objects they
live in.

This is especially useful when rendering web pages as during this
rendering often the same data are used again and again, whereas you don't
know at the beginning of the rendering process which data you will really
need.

We first need a function that will be used to provide a value
for our lazy variable. This function will expect one parameter that will
be set to the LazyVars object when the function is called.

Our demonstration function will increment a counter on a context object
(provided via the vars parameter) and return this counter so that we can easily
follow the calls to the function:

  >>> def getNumber(vars):
  ...     context = vars.context
  ...     context.counter += 1
  ...     return context.counter

We now register the function with our LazyVars class under the name we later
want to use for accessing the variable:

  >>> from cybertools.lazyvars.lazyvars import LazyVars
  >>> LazyVars.registerVariable('number', getNumber)

We also need a context object - that one which carries the above mentioned
counter:

  >>> class Number(object):
  ...    counter = 0
  >>> context = Number()

This object is now used as the context parameter when creating a LazyVars
object:
  
  >>> lv = LazyVars(context)

So let's look if the LazyVars object can give us a value for the variable
we have registered:

  >>> lv.number
  1

The getNumber() function has been called that apparently has
incremented the counter.

What happens if we access the variable again?

  >>> lv.number
  1

Same result, no incrementation, as it is now stored in the LazyVars object and
retrieved without recalculation. Really lazy...

We can even use the same function for more than one variable. When we first
access the new variable the function is called again:

  >>> LazyVars.registerVariable('number2', getNumber)
  >>> lv.number2
  2

Our first variable is not affected by this:

  >>> lv.number
  1
  
