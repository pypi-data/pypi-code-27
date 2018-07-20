# -*- coding: utf-8 -*-
# @Date    : 2018-07-20 10:05:57
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from plone.api.validation import required_parameters

import six


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


@required_parameters('value')
def force_unicode(value, allow_non_str=True):
    """ """
    if not isinstance(value, six.string_types):
        if not allow_non_str:
            return value
        else:
            value = str(value)

    if isinstance(value, bytes):
        return value.decode('utf-8', 'strict')

    if six.PY2:
        if not isinstance(value, unicode):
            return value.decode('utf-8', 'strict')

    return value


@required_parameters('string')
def force_bytes(string, encoding='utf-8', errors='strict'):

    if isinstance(string, bytes):
        if encoding == 'utf-8':
            return string
        else:
            return string.decode('utf-8', errors).encode(encoding, errors)

    if not isinstance(string, six.string_types):
        return string

    return string.encode(encoding, errors)
