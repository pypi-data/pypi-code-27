import functools as ft

def compose(*fs):
  def compose2(f, g):
    return lambda x: f(g(x))
  return ft.reduce(compose2, fs, lambda x: x)

def curry(f):
  """
  Coded by Massimiliano Tomassoli, 2012.

  - Thanks to b49P23TIvg for suggesting that I should use a set operation
      instead of repeated membership tests.
  - Thanks to Ian Kelly for pointing out that
      - "minArgs = None" is better than "minArgs = -1",
      - "if args" is better than "if len(args)", and
      - I should use "isdisjoint".
  https://mtomassoli.wordpress.com/2012/03/18/currying-in-python/
  https://gist.github.com/JulienPalard/021f1c7332507d6a494b
  Decorator to curry a function, typical usage:

  >>> @curry
  ... def foo(a, b, c):
  ...    return a + b + c

  The function still work normally:
  >>> foo(1, 2, 3)
  6

  And in various curried forms:
  >>> foo(1)(2, 3)
  6
  >>> foo(1)(2)(3)
  6

  This also work with named arguments:
  >>> foo(a=1)(b=2)(c=3)
  6
  >>> foo(b=1)(c=2)(a=3)
  6
  >>> foo(a=1, b=2)(c=3)
  6
  >>> foo(a=1)(b=2, c=3)
  6

  And you may also change your mind on named arguments,
  But I don't know why you may want to do that:
  >>> foo(a=1, b=0)(b=2, c=3)
  6

  Finally, if you give more parameters than expected, the exception
  is the expected one, not some garbage produced by the currying
  mechanism:

  >>> foo(1, 2)(3, 4)
  Traceback (most recent call last):
     ...
  TypeError: foo() takes exactly 3 arguments (4 given)
  """
  def curried(*args, **kwargs):
    if len(args) + len(kwargs) >= f.__code__.co_argcount:
      return f(*args, **kwargs)
    return (lambda *args2, **kwargs2: curried(*(args + args2), **dict(kwargs, **kwargs2)))

  return curried

def identity(i):
  """ f[A A](A => A): A"""
  return i