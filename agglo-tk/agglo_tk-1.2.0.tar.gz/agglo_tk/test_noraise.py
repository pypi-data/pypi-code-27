from no_raise import no_raise

def foo(param):
  raise Exception("foo error")

def test():
  assert no_raise(foo, 1)
