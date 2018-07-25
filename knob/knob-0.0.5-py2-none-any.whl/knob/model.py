# -*- coding:utf-8 -*-

import six


def update_model(obj, para, fields=None):
    updated_fields = set()
    for key, val in six.iteritems(para):
        if fields is None or key in fields:
            setattr(obj, key, val)
        updated_fields.add(key)

    if updated_fields:
        obj.save(updated_fields=list(updated_fields))

    return obj

