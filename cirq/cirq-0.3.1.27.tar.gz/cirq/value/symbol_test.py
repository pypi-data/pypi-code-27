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
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from cirq.value import Symbol
from cirq.testing import EqualsTester


def test_parameterized_value_init():
    assert Symbol(u'a').name == u'a'
    assert Symbol(u'b').name == u'b'

def test_string_representation():
    assert unicode(Symbol(u'a1')) == u'a1'
    assert unicode(Symbol(u'_b23_')) == u'_b23_'
    assert unicode(Symbol(u'1a')) == u'Symbol("1a")'
    assert unicode(Symbol(u'&%#')) == u'Symbol("&%#")'
    assert unicode(Symbol(u'')) == u'Symbol("")'

def test_parameterized_value_eq():
    eq = EqualsTester()
    eq.add_equality_group(Symbol(u'a'))
    eq.make_equality_group(lambda: Symbol(u'rr'))
