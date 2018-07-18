import logging
import time

from six import get_method_function, get_method_self, wraps

FALLBACK_LOGGER = logging.getLogger(__name__).getChild("fallback")


def call_sig(args, kwargs):
    """Generates a function-like signature of function called with certain parameters.

    Args:
        args: *args
        kwargs: **kwargs

    Returns:
        A string that contains parameters in parentheses like the call to it.
    """
    arglist = [repr(x) for x in args]
    arglist.extend("{}={!r}".format(k, v) for k, v in kwargs.items())
    return "({args})".format(args=", ".join(arglist))


def logged(_missused=False, log_args=False, log_result=False):
    """Decorator that logs entry and exit to a method and also times the execution.

    It assumes that the object where you decorate the methods on
    has a ``.logger`` attribute.

    Args:
        log_args: Whether to log args passed to the method
        log_result: Whether to log the result value returned from the method.
    """

    def g(f):
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            start_time = time.time()
            signature = f.__name__ + (call_sig(args, kwargs) if log_args else "")
            log = getattr(self, "logger", FALLBACK_LOGGER)
            log.debug("%s started", signature)
            try:
                result = f(self, *args, **kwargs)
            except Exception as e:
                elapsed_time = (time.time() - start_time) * 1000.0
                log.error(
                    "An exception happened during %s call (elapsed %.0f ms)",
                    signature,
                    elapsed_time,
                )
                log.exception(e)
                raise
            else:
                elapsed_time = (time.time() - start_time) * 1000.0
                if log_result:
                    log.info(
                        "%s -> %r (elapsed %.0f ms)", signature, result, elapsed_time
                    )
                else:
                    log.info("%s (elapsed %.0f ms)", signature, elapsed_time)
                return result

        wrapped.original_function = f
        return wrapped

    return g


def call_unlogged(method, *args, **kwargs):
    """Calls the original method without logging when ``logged`` is applied.

    In case you pass in an ordinary method that was not decorated,
    it will work as usual.

    Args:
        method: The method object from the object.
        *args: Args to pass to the method.
        **kwargs: Keyword arguments to pass to the method.

    Returns:
        Whatever that method returns.
    """
    try:
        f = method.original_function
    except AttributeError:
        f = get_method_function(method)

    return f(get_method_self(method), *args, **kwargs)
