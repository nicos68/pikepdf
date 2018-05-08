# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2017, James R. Barlow (https://github.com/jbarlow83/)

"""Provide classes to stand in for PDF objects

The purpose of these is to provide nice-looking classes to allow explicit
construction of PDF objects and more pythonic idioms and facilitate discovery
by documentation generators.

It's also a place to narrow the scope of input types to those more easily 
converted to C++.

In reality all of these return objects of class pikepdf.Object or rather 
QPDFObjectHandle which is a generic type.

"""

from decimal import Decimal, InvalidOperation
from math import isfinite

from . import _qpdf
from ._qpdf import Object, ObjectType


class _ObjectMeta(type):
    "Supports instance checking"

    def __instancecheck__(cls, instance):
        if type(instance) != Object:
            return False
        return cls.object_type == instance.type_code


class Boolean(metaclass=_ObjectMeta):
    object_type = ObjectType.boolean

    def __new__(cls, value):
        return _qpdf._new_boolean(value)


class Integer(metaclass=_ObjectMeta):
    object_type = ObjectType.integer

    def __new__(cls, n):
        if n.bit_length() >= 64:
            raise ValueError('Value is too large for 64-bit integer')
        return _qpdf._new_integer(n)


class Real(metaclass=_ObjectMeta):
    object_type = ObjectType.real

    def __new__(cls, value, dec_places=0):
        if dec_places < 0 or not isinstance(dec_places, int):
            raise ValueError('dec_places must be nonnegative integer')

        if isinstance(value, int):
            return _qpdf._new_real(value, 0)
        
        if isinstance(value, float) and isfinite(value):
            return _qpdf._new_real(value, dec_places)

        try:
            dec = Decimal(value)
        except InvalidOperation:
            raise TypeError('Could not convert object to int, float or Decimal')

        if dec.is_infinite() or dec.is_nan():
            raise ValueError('NaN and infinity are not valid PDF objects')

        return _qpdf._new_real(str(dec))
        

class Name(metaclass=_ObjectMeta):
    object_type = ObjectType.name

    def __new__(cls, name):
        return _qpdf._new_name(name)


class String(metaclass=_ObjectMeta):
    object_type = ObjectType.string

    def __new__(cls, s):
        return _qpdf._new_string(s)