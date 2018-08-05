# -*- coding: utf-8 -*-

class TakumiHttpException(Exception):
    """Base exception class of takumi_http.
    """


class PayloadInvalid(TakumiHttpException):
    """Raised when http payload has invalid format.
    """
