# -*- coding: utf-8 -*-
"""
Module defining classes for describing the parameters of the actions.

The parameter classes contain the definition of the parameter (name,
description, type) but also the mechanism to convert the specified
values for the parameter (most of the time these are text values read
from a file or received from a socket) into actual values that can be
used by the action (numbers, dates, etc.)
"""

SINGLE_TEXT_FIELD = u"single-text-field"
"""
Form type for the parameters whose value is a single text value.

This type can be used in the GUI to correctly display the form where
the user gives a value for the parameter.

Type: :class:`str`
"""
MULTIPLE_TEXT_COUPLES_FIELD = u"multiple-text-couples-field"
"""
Form type for the parameters whose value is a list of couples of text values.

This type can be used in the GUI to correctly display the form where
the user gives a value for the parameter.

Type: :class:`str`
"""


class AbstractParameter(object):
    form_type = None

    def __init__(self, uid, name, desc, type_desc):
        self.uid = uid
        self.name = name
        self.desc = desc
        self.type_desc = type_desc
        if self.__class__ is AbstractParameter:
            raise NotImplementedError(u"Abstract class can't be implemented")

    def _get_def_value(self):
        raise NotImplementedError(u"Abstract method can't be called")

    def _convert(self, specif_val):
        raise NotImplementedError(u"Abstract method can't be called")

    def dump(self):
        return {u"uid": self.uid,
                u"name": self.name,
                u"desc": self.desc,
                u"typeDesc": self.type_desc,
                u"formType": self.form_type}

    def build_value(self, specif_val):
        if specif_val is None:
            return self._get_def_value()
        else:
            return self._convert(specif_val)

    def log_value(self, value):
        return (self.name, u"{0}".format(value))


class SingleParameter(AbstractParameter):
    form_type = SINGLE_TEXT_FIELD

    def __init__(self, uid, name, desc, type_desc,
                 type_conv, def_value=None):
        super(SingleParameter, self).__init__(uid, name, desc, type_desc)
        self._type_conv = type_conv
        self._def_value = def_value

    def _get_def_value(self):
        return self._def_value

    def _convert(self, specif_val):
        try:
            value = self._type_conv(specif_val)
        except ValueError:
            raise ValueError(u"Can't convert to target type with {0} from: {1}"
                             u"".format(self._type_conv, specif_val))
        return value


class CouplesParameter(AbstractParameter):
    form_type = MULTIPLE_TEXT_COUPLES_FIELD

    def __init__(self, uid, name, desc, type_desc,
                 type_conv_1, type_conv_2, def_value=None):
        super(CouplesParameter, self).__init__(uid, name, desc, type_desc)
        self._type_conv_1 = type_conv_1
        self._type_conv_2 = type_conv_2
        self._def_value = def_value

    def _get_def_value(self):
        if isinstance(self._def_value, (tuple, list)):
            return list(self._def_value)[:]
        else:
            return self._def_value

    def _convert(self, specif_val):
        couples = []
        if not isinstance(specif_val, (tuple, list)):
            raise ValueError(u"Expects a list of couples and got: {0}"
                             u"".format(specif_val))
        for elts in specif_val:
            try:
                elt_1, elt_2 = elts
            except ValueError:
                raise ValueError(u"Expects a list of couples and got: {0}"
                                 u"".format(specif_val))
            try:
                val_1 = self._type_conv_1(elt_1)
            except ValueError:
                raise ValueError(
                    u"Can't convert to target type with {0} from: "
                    u"{1}".format(self._type_conv_1, elt_1))
            try:
                val_2 = self._type_conv_2(elt_2)
            except ValueError:
                raise ValueError(
                    u"Can't convert to target type with {0} from: "
                    u"{1}".format(self._type_conv_2, elt_2))
            couples.append((val_1, val_2))
        return couples

    def log_value(self, value):
        return (self.name, u"\n".join([u"{0}: {1}".format(elt_1, elt_2)
                                       for (elt_1, elt_2) in value]))
