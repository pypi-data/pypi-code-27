import sys
import inspect
from numba import jit as actual_jit

def sphinx_compat_jit(f_or_has_args=None, **kwargs):
    """To be used instead of @jit in order to prevent jit from rewriting
    obscure parts of the function's documentation (to contain e.g. unquoted
    asterisks) when sphinx is trying to read it.

    should not change jit functionlity if you are not sphinx."""
    def jit_passthru(f):
        return actual_jit(f, **kwargs)
    def do_nothing(f):
        return f
    # returns one "FrameInfo" object per stack frame
    stack = inspect.stack()
    # get the "name" of each frame's calling module, as in
    # https://stackoverflow.com/questions/7871319/how-to-know-who-is-importing-me-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    modules = [finfo.frame.f_globals.get('__name__') for finfo in stack]
    # if sphinx_compat_jit was used as a decorator with no parameters
    # or as a regular function
    if f_or_has_args is not None:
        if 'sphinx' in modules:
            return f_or_has_args
        else:
            return actual_jit(f_or_has_args, **kwargs)
    # otherwise it was used as a decorator with parameters
    else:
        if 'sphinx' in modules:
            actual_decorator = do_nothing
        else:
            actual_decorator = jit_passthru
    return actual_decorator
