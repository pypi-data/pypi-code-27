import re
import math
from typing import Dict, Any, Sequence, Callable, Pattern, Union

from funkpy import Collection as _


def __regTest__(regex: Pattern) -> Callable[[str], bool]:
  reg = re.compile(regex)

  def test(string: str) -> bool:
    res = reg.search(string)
    return  True if res != None and res.group(0) != "" else False

  return test

def apply(func: Callable, item: Any) -> Any: 
  return func(item)

def isGood(func: Callable, item: Any) -> bool:
  return func(item) is True

def pick(keys: Sequence[str], doc: Dict) -> Dict:
  """Picks the provided keys from the dictionary.
  
  Example
    pick(["a", "b"], {"a": 1, "b": 2, "c": 3}) # => {"a": 1, "b": 2}
  """

  if not _.isIterable(keys):
    return None

  if not isinstance(doc, dict):
    return None

  return {k: doc.get(k, None) for k in keys}

def pickRegex(keys: Sequence[str], doc: Dict) -> Dict:
  if not isinstance(doc, dict):
    return None

  regex_keys = _.map(__regTest__, keys)
    
  return pick(
    _.filter(lambda k: sum(_.map(lambda reg: reg(k), regex_keys))>0, doc.keys() ),
    doc
  )

def get(doc: Dict, key: str) -> Union[Any, None]:
  """Gets the value for key from the dictionary.
  
  Example
    get("a", {"a": 1, "b": 2, "c": 3}) # => 1
  """

  if not isinstance(doc, dict):
    return None

  if not isinstance(key, str):
    return None

  return doc.get(key, None)

def getValues(doc, keys):
  if not _.isIterable(keys):
    return None
  return _.map(lambda k: get(doc, k), keys)

def update(doc: Dict, new_doc: Dict) -> Dict:
  """ Updates a dictionary without side-effects.
  
  Example
    dc = {"a": 1, "b": 2, "c": 3}
    newDC = update(dc, {"d": 4})
    newDC = update(newDC, ("e", 5)) # => {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
  """
  if not isinstance(doc, dict):
    return None

  d = doc.copy()
  return d.update(new_doc) or d



class Item:

  def __init__(self, data=None):
    if data != None: 
      self.val = data

  @staticmethod
  def of(data=None):
    return Item(data)

  def filter(self, func):
    return self.of(isGood(func, self.val))

  def map(self, func):
    return self.of(apply(func, self.val))
  
  def apply(self, func):
    return self.of(func(self.val))
  
  def pick(self, keys):
    return self.of(pick(keys, self.val))

  def pickRegex(self, keys):
    return self.of(pickRegex(keys, self.val))

  def get(self, key):
    return get(self.val, key)

  def getValues(self, keys):
    return getValues(self.val, keys)


class exports:
  """ This class contains all public methods which can be used directly."""

  apply = apply
  pick = pick
  isGood = isGood
  pickRegex = pickRegex
  get = get
  getValues = getValues
  update = update