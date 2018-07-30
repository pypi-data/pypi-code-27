import functools


def do(before=None, after=None):
    def decorator(func):
        def new_func(*args, **kwargs):
            is_continue = True

            if before:
                r = before(*args, **kwargs)
                # return value of before() can stop the steps
                if r is False:
                    is_continue = False

            if is_continue:
                rv = func(*args, **kwargs)
                # only called if function have return value
                if after and rv:
                    # add the return value to keyword parameters as 'rv'
                    kwargs['rv'] = rv
                    # call after()
                    after(*args, **kwargs)
                return rv

        return new_func

    return decorator


do_before = functools.partial(do, after=None)
do_after = functools.partial(do, before=None)
