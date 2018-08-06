import functools as ft
import builtins 
# from typing import TypeVar, Iterable, Tuple
from collections import abc
# from funkpy.utils import curry, compose

def __getClass__(iterable):
  if type(iterable).__name__ == "dict_keys":
    return list
  else:
    return getattr(builtins, type(iterable).__name__, list)

def __zip__(*iterables):
  """Zips a tuple of iterables.
  
  Arguments:
    iterables {tuple} -- N arguments
  
  Yields:
    iterable
  """

  target_class = __getClass__(iterables[0])
  sentinel = object()
  iterators = [iter(it) for it in iterables]

  while iterators:
    result = []
    for it in iterators:
      elem = next(it, sentinel)
      if elem is sentinel:
        return
      result.append(elem)

    yield target_class(result)

def __filter__(func, iterable):
  return __getClass__(iterable)(builtins.filter(func, iterable))

def __map__(func, *iterables): 
  return __getClass__(iterables[0])(builtins.map(func, *iterables))

def isIterable(value):
  """ Checks if the value implements iterator interface.

  Arguments:
    value {any}
  Return:
    boolean
  """
  # return hasattr(value, '__iter__')
  return isinstance(value, abc.Iterable)

def isSubscriptable(value):
  """ Checks if the value is subscriptable.

  Arguments:
    value {any}
  Return:
    boolean
  """
  return hasattr(value, '__getitem__')

def isMutable(seq):
  return isinstance(seq, abc.MutableSequence)

def isList(value):
  """ Checks if the value is a python list.

  Arguments:
    value {list}
  Return:
    boolean
  """
  return isIterable(value) and isSubscriptable(value)

class exports:

  isIterable = isIterable
  isSubscriptable = isSubscriptable
  isMutable = isMutable
  isList = isList

  @staticmethod
  def zip(*iterables):
    """ Zips collections together. 

    The collections can be of different length.

    Examples:
      # zip lists
      zip([1, 2, 3] # =>[[1], [2], [3]]
      zip([1, 2, 3], [1, 2, 3]) # => [[1, 1], [2, 2], [3, 3]]
      zip(*[[1, 2, 3], [1, 2, 3]]) # => [[1, 1], [2, 2], [3, 3]]

      # zip tupel
      zip((1, 2, 3)) # => ((1,), (2,), (3,))
      zip((1, 2, 3), (1, 2, 3)) # => ((1, 1), (2, 2), (3, 3))
    
    Arguments:
      iterables {tuple} -- N arguments
    Returns:
      collection
    """
    target_class = __getClass__(iterables[0])
    
    if target_class == set:
      # It is not possible to construct a set of sets!
      target_class = list

    return target_class(__zip__(*iterables))

  @staticmethod
  def map(func, *iterables):
    """ Applies a function on each element of the collection and returns a new collection.
    
    Arguments:
      func      {function}
      iterables {tuple}    -- N arguments
    
    Returns:
      collection
    """
    return __map__(func, *iterables)

  @staticmethod
  def strictMap(func, iterable):
    """ Applies a function on each element of the collection and returns a new collection. 
    It is faster that collection.map

    Arguments:
      func     {fucntion}
      iterable {collection}

    Returns:
      collection
    """
    return __getClass__(iterable)(func(i) for i in iterable)

  @staticmethod
  def forEach(func, *iterables):
    """ Applies a function on each element of the collection.
    
    Examples:
      newList = []
      forEach(lambda i: newList.append(i + 1), [1, 2, 3]) or newList # => [2, 3, 4]
    
    Arguments:
      func      {func} 
      iterables {tuple} -- N arguments

    Returns:
      None
    """
    __map__(func, *iterables)
    return None

  @staticmethod
  def reduce(func, arr, agg):
    return ft.reduce(func, arr, agg)

  @staticmethod
  def concat(*args):
    if (len(args)==0): 
      return []
    
    arr = args[0]
    if isIterable(arr) == False:
      arr = [arr]

    target_class = __getClass__(arr)

    if isMutable(arr) == False:
      arr = list(arr)

    return target_class(ft.reduce(
      lambda agg, item: (agg.extend(item) if isIterable(item) else agg.append(item)) or agg, \
      args[1:], \
      arr.copy() if isMutable(arr) else list(arr)
    ))

  @staticmethod
  def flatten(seq):
    """Flattens a sequenece. The type of the first element determines return type
    
    Arguments:
      seq {collection} -- list, tupple or set
    
    Returns:
      collection
    """
    return exports.concat(*seq)

  @staticmethod
  def push(arr=None, *args):
    return ft.reduce(lambda agg, item: agg.append(item) or agg, args, arr.copy() if (arr and isList(arr)) else [])

  @staticmethod
  def filter(func, arr):
    return __filter__(func, arr)
