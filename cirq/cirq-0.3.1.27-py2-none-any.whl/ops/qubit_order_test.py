# coding=utf-8
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" qubit_order,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import with_statement
from __future__ import absolute_import
import pytest

from cirq.ops.qubit_order import default_sorting_key
from cirq.ops import QubitOrder, NamedQubit


def test_default_sorting_key():
    assert default_sorting_key(u'') == u''
    assert default_sorting_key(u'a') == u'a'
    assert default_sorting_key(u'a0') == u'a00000000:1'
    assert default_sorting_key(u'a00') == u'a00000000:2'
    assert default_sorting_key(u'a1bc23') == u'a00000001:1bc00000023:2'
    assert default_sorting_key(u'a9') == u'a00000009:1'
    assert default_sorting_key(u'a09') == u'a00000009:2'
    assert default_sorting_key(u'a00000000:8') == u'a00000000:8:00000008:1'


def test_sorted_by_default_sorting_key():
    actual = [
        u'',
        u'1',
        u'a',
        u'a00000000',
        u'a00000000:8',
        u'a9',
        u'a09',
        u'a10',
        u'a11',
    ]
    assert sorted(actual, key=default_sorting_key) == actual
    assert sorted(reversed(actual), key=default_sorting_key) == actual


def test_default():
    a2 = NamedQubit(u'a2')
    a10 = NamedQubit(u'a10')
    b = NamedQubit(u'b')
    assert QubitOrder.DEFAULT.order_for([]) == ()
    assert QubitOrder.DEFAULT.order_for([a10, a2, b]) == (a2, a10, b)


def test_explicit():
    a2 = NamedQubit(u'a2')
    a10 = NamedQubit(u'a10')
    b = NamedQubit(u'b')
    with pytest.raises(ValueError):
        _ = QubitOrder.explicit([b, b])
    q = QubitOrder.explicit([a10, a2, b])
    assert q.order_for([b]) == (a10, a2, b)
    assert q.order_for([a2]) == (a10, a2, b)
    assert q.order_for([]) == (a10, a2, b)
    with pytest.raises(ValueError):
        _ = q.order_for([NamedQubit(u'c')])


def test_explicit_with_fallback():
    a2 = NamedQubit(u'a2')
    a10 = NamedQubit(u'a10')
    b = NamedQubit(u'b')
    q = QubitOrder.explicit([b], fallback=QubitOrder.DEFAULT)
    assert q.order_for([]) == (b,)
    assert q.order_for([b]) == (b,)
    assert q.order_for([b, a2]) == (b, a2)
    assert q.order_for([a2]) == (b, a2)
    assert q.order_for([a10, a2]) == (b, a2, a10)


def test_sorted_by():
    a = NamedQubit(u'2')
    b = NamedQubit(u'10')
    c = NamedQubit(u'-5')

    q = QubitOrder.sorted_by(lambda e: -int(unicode(e)))
    assert q.order_for([]) == ()
    assert q.order_for([a]) == (a,)
    assert q.order_for([a, b]) == (b, a)
    assert q.order_for([a, b, c]) == (b, a, c)


def test_map():
    b = NamedQubit(u'b!')
    q = QubitOrder.explicit([NamedQubit(u'b')]).map(
        internalize=lambda e: NamedQubit(e.name[:-1]),
        externalize=lambda e: NamedQubit(e.name + u'!'))

    assert q.order_for([]) == (b,)
    assert q.order_for([b]) == (b,)


def test_qubit_order_or_list():
    b = NamedQubit(u'b')

    implied_by_list = QubitOrder.as_qubit_order([b])
    assert implied_by_list.order_for([]) == (b,)

    implied_by_generator = QubitOrder.as_qubit_order(
        NamedQubit(e.name + u'!') for e in [b])
    assert implied_by_generator.order_for([]) == (NamedQubit(u'b!'),)
    assert implied_by_generator.order_for([]) == (NamedQubit(u'b!'),)

    ordered = QubitOrder.sorted_by(repr)
    passed_through = QubitOrder.as_qubit_order(ordered)
    assert ordered is passed_through
