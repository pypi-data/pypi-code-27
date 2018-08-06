class Functor:
  """ A container with a map interface. """

  def __init__(self, value=None):
    self.val = value

  def __eq__(self, other):
    if isinstance(other, Functor):
      return self.val == other.val
    else:
      return self.val == other

  def __str__(self):
    return str(self.val)

  @staticmethod
  def of(value):
    """ Class constructor fucntion.
    A => F[A]

    Arguments:
      val {A} -- any value type

    Returns:
      F[A] -- option of any value type
    """
    return Functor(value)

  def map(self, func):
    """ (F[A], A => B) => F[B]

    Transforms the value inside the container

    Arguments:
      func {Function} -- Any function A => B

    Returns:
      F[B]
    """
    return Functor.of(func(self.val))


class Monad(Functor):
  """ A container with a `flatMap` and `of` interfaces. """

  @staticmethod
  def of(val):
    """ Class constructor fucntion. Also known as `pure`.
    A => M[A]

    Arguments:
      val {A} -- any value type

    Returns:
      M[A] -- option of any value type
    """
    return Monad(val)
 
  def flatMap(self, func):
    """ (M[A], A => M[B]) => M[B]

    The conventional defintion of flatMap requres it to return M[B].
    In type-safe languages that condition can be easily enforced
    but in Python this is not possible without hard-wiring these checks.
    Hence, this implementation shall not enforce this rule and allow users 
    to unwrap the monad by using 
      func[A, B] (A => B): B
      i.e. 
      monad.flatMap(lambda i: i)
    
    It is up to the developer to decide whether they want to be strict about it.

    Arguments:
      func {Function} -- A => M[B]

    Returns:
      M[B]
    """
    return func(self.val)

class Either(Monad):
  """[summary]
  
  [description]
  """

  @staticmethod
  def of(val):
    """ Class constructor method.
    A => F[A]

    Arguments:
      val {A} -- any value type

    Returns:
      F[A] -- option of any value type
    """
    if isinstance(val, Exception) or val is None:
      return Either.Left(val)
    return Either.Right(val)

  @staticmethod
  def Left(val):
    return Either([val])

  @staticmethod
  def Right(val):
    return Either([None, val])

  def flatMap(self, func):
    """ (M[A], A => M[B]) => M[B]

    Arguments:
      func {Function} -- A => M[B]
    """
    return self if len(self.val) == 1 else func(self.val[1])

  def map(self, func):
    """ (M[A], A => B) => M[B]

    Transforms the value inside the monad

    Arguments:
      func {Function} -- Any function A => B
    """
    return self if len(self.val) == 1 else self.of(func(self.val[1]))

  def either(self, left_func, right_func):
    """Unwraps the container and executes either left_func or right_func depending on the value inside
    
    Arguments:
      left_func  {Function} -- [description]
      right_func {Function} -- [description]
        """
    if len(self.val) == 1:
      return left_func(self.val[0])
    else:
      return right_func(self.val[1])


class Option(Monad):

  Nothing = None
  """ Internal reference to empty value."""

  @staticmethod
  def of(val):
    """ Class constructor function.
    A => M[A]

    Arguments:
      val {A} -- any value type

    Returns:
      M[A] -- option of any value type
    """
    return Option(val)

  def flatMap(self, func):
    """ (M[A], A => M[B]) => M[B]

    Arguments:
      func {Function} -- A => M[B]
    """
    return self if self == Option.Nothing else func(self.val)

  def map(self, func):
    """ (M[A], A => B) => M[B]

    Transforms the value inside the container

    Arguments:
      func {Function} -- Any function A => B
    """
    # return self if self.val == Option.Nothing else Option.of(func(self.val))
    return self if self == Option.Nothing else self.flatMap(lambda i: self.of(func(i)))

  def maybe(self, val2=None):
    """ Returns either the value inside the container or val2. """

    return val2 if self == Option.Nothing else self.val
