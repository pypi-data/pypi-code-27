
class ProtoTypeDict(dict):
  def __init__(self, prefix, key_serializer, serializer):
    self.prefix = prefix
    self.serializer = serializer
    self.key_serializer = key_serializer

  def get(self, key, default=None):
    if key in self:
      return self[key]
    return default

  def keys(self):
    return [k for k in self.iterkeys()]

  def values(self):
    return [v for k,v in self.iteritems()]

  def items(self):
    return list(self.iteritems())

  def iteritems(self):
    for key in self.iterkeys():
      yield (key, self[key])

  def __iter__(self):
    return self.iterkeys()

  def __len__(self):
    return len(self.keys())

  def update(self, other_dict):
    for k, v in other_dict.iteritems():
      self[k] = v

  def _strip_key_prefix_and_decode(self, key):
    return self.key_serializer.decode(key[len(self.prefix):])

  def __repr__(self):
    return dict(self.iteritems()).__repr__()

  def __eq__(self, other):
      if isinstance(other, dict):
        for k,v in other.iteritems():
          if k not in self or self[k] != v:
            return False
        return True
      return False

  def __ne__(self, other):
    return not self == other