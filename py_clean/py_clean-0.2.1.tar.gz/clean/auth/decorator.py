from typing import Dict

from clean.exceptions import AuthException
from clean.auth.abs import DecodeToken

import logging


def create_decorator(v_class, token_finder, debug=False, logger=logging):
    def protect(user: Dict = None, rule: Dict = None, allow_super: bool = False):
        def wrap(f):
            def wrapped_f(*args, **kwargs):
                if debug:
                    return f(*args, **kwargs)
                context = token_finder()
                kwargs_perm = dict(user=user, rule=rule, allow_super=allow_super)
                dt = v_class(raw_token=context, kwargs_perm=kwargs_perm)
                try:
                    dt.is_valid()
                    kwargs['user_token'] = dt.user_token
                    return f(*args, **kwargs)
                except AuthException as e:
                    info = dict(toke=context, perms=kwargs_perm)
                    logger.info("invalid token", info)
                    return dt.create_resp_err(str(e))
            return wrapped_f
        return wrap
    return protect


class DecoratorBuilder:

    def __init__(self, verify_class, token_finder_func, debugging=False, logger=logging):
        self.verify_class = verify_class
        self.token_finder_func = token_finder_func
        self.debugging = debugging

        self.verify_decode_class()
        self.verify_token_finder()
        self.logger = logger

    def verify_decode_class(self):
        if not issubclass(self.verify_class, DecodeToken):
            raise AttributeError('verify_class is not subclass of "DecodeToken"')

    def verify_token_finder(self):
        if not callable(self.token_finder_func):
            raise AttributeError('token_finder_func is not callable')

    def create(self):
        return create_decorator(self.verify_class, self.token_finder_func, debug=self.debugging, logger=self.logger)
