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
from __future__ import with_statement
from __future__ import absolute_import
import pytest

from cirq.api.google.v1.params_pb2 import (
    ParameterSweep,
    ZipSweep,
    SingleSweep,
)
from cirq.google import params
from cirq.study.sweeps import Linspace, Points, Product, Unit, Zip


def test_gen_sweep_points():
    points = [0.5, 1.0, 1.5, 2.0, 2.5]
    sweep = SingleSweep()
    sweep.parameter_key = u'foo'
    sweep.points.points.extend(points)
    out = params._sweep_from_single_param_sweep(sweep)
    assert out == Points(u'foo', [0.5, 1.0, 1.5, 2.0, 2.5])


def test_gen_sweep_linspace():
    sweep = SingleSweep()
    sweep.parameter_key = u'bar'
    sweep.linspace.first_point = 0
    sweep.linspace.last_point = 10
    sweep.linspace.num_points = 11
    out = params._sweep_from_single_param_sweep(sweep)
    assert out == Linspace(u'bar', 0, 10, 11)


def test_gen_param_sweep_zip():
    sweep = ZipSweep()
    s1 = sweep.sweeps.add()
    s1.parameter_key = u'foo'
    s1.points.points.extend([1, 2, 3])
    s2 = sweep.sweeps.add()
    s2.parameter_key = u'bar'
    s2.points.points.extend([4, 5])
    out = params._sweep_from_param_sweep_zip(sweep)
    assert out == Points(u'foo', [1, 2, 3]) + Points(u'bar', [4, 5])


def test_gen_empty_param_sweep():
    ps = ParameterSweep()
    out = params.sweep_from_proto(ps)
    assert out == Unit


def test_gen_param_sweep():
    ps = ParameterSweep()
    f1 = ps.sweep.factors.add()
    s1 = f1.sweeps.add()
    s1.parameter_key = u'foo'
    s1.points.points.extend([1, 2, 3])
    f2 = ps.sweep.factors.add()
    s2 = f2.sweeps.add()
    s2.parameter_key = u'bar'
    s2.points.points.extend([4, 5])
    out = params.sweep_from_proto(ps)
    assert out == Product(Zip(Points(u'foo', [1, 2, 3])),
                          Zip(Points(u'bar', [4, 5])))


def test_empty_param_sweep_keys():
    ps = ParameterSweep()
    assert params.sweep_from_proto(ps).keys == []


def test_param_sweep_keys():
    ps = ParameterSweep()
    f1 = ps.sweep.factors.add()
    s11 = f1.sweeps.add()
    s11.parameter_key = u'foo'
    s11.points.points.extend(xrange(5))
    s12 = f1.sweeps.add()
    s12.parameter_key = u'bar'
    s12.points.points.extend(xrange(7))
    f2 = ps.sweep.factors.add()
    s21 = f2.sweeps.add()
    s21.parameter_key = u'baz'
    s21.points.points.extend(xrange(11))
    s22 = f2.sweeps.add()
    s22.parameter_key = u'qux'
    s22.points.points.extend(xrange(13))
    out = params.sweep_from_proto(ps)
    assert out.keys == [u'foo', u'bar', u'baz', u'qux']


def test_empty_param_sweep_size():
    ps = ParameterSweep()
    assert len(params.sweep_from_proto(ps)) == 1


def test_param_sweep_size():
    ps = ParameterSweep()
    f1 = ps.sweep.factors.add()
    s11 = f1.sweeps.add()
    s11.parameter_key = u'11'
    s11.linspace.num_points = 5
    s12 = f1.sweeps.add()
    s12.parameter_key = u'12'
    s12.points.points.extend(xrange(7))
    f2 = ps.sweep.factors.add()
    s21 = f2.sweeps.add()
    s21.parameter_key = u'21'
    s21.linspace.num_points = 11
    s22 = f2.sweeps.add()
    s22.parameter_key = u'22'
    s22.points.points.extend(xrange(13))
    assert len(params.sweep_from_proto(ps)) == 5 * 11


def test_param_sweep_size_no_sweeps():
    ps = ParameterSweep()
    ps.sweep.factors.add()
    ps.sweep.factors.add()
    assert len(params.sweep_from_proto(ps)) == 0


def example_sweeps():
    empty_sweep = ParameterSweep()

    empty_product = ParameterSweep()

    empty_zip = ParameterSweep()
    empty_zip.sweep.factors.add()
    empty_zip.sweep.factors.add()

    full_sweep = ParameterSweep()
    f1 = full_sweep.sweep.factors.add()
    s11 = f1.sweeps.add()
    s11.parameter_key = u'11'
    s11.linspace.first_point = 0
    s11.linspace.last_point = 10
    s11.linspace.num_points = 5
    s12 = f1.sweeps.add()
    s12.parameter_key = u'12'
    s12.points.points.extend(xrange(7))

    f2 = full_sweep.sweep.factors.add()
    s21 = f2.sweeps.add()
    s21.parameter_key = u'21'
    s21.linspace.first_point = 0
    s21.linspace.last_point = 10
    s21.linspace.num_points = 11
    s22 = f2.sweeps.add()
    s22.parameter_key = u'22'
    s22.points.points.extend(xrange(13))

    return [empty_sweep, empty_product, empty_zip, full_sweep]


@pytest.mark.parametrize(u'param_sweep', example_sweeps())
def test_param_sweep_size_versus_gen(param_sweep):
    sweep = params.sweep_from_proto(param_sweep)
    predicted_size = len(sweep)
    out = list(sweep)
    assert len(out) == predicted_size


@pytest.mark.parametrize(u'sweep,expected', [
    (
        Unit,
        Unit
    ),
    (
        Linspace(u'a', 0, 10, 25),
        Product(Zip(Linspace(u'a', 0, 10, 25)))
    ),
    (
        Points(u'a', [1, 2, 3]),
        Product(Zip(Points(u'a', [1, 2, 3])))
    ),
    (
        Zip(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3])),
        Product(Zip(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3]))),
    ),
    (
        Product(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3])),
        Product(Zip(Linspace(u'a', 0, 1, 5)), Zip(Points(u'b', [1, 2, 3]))),
    ),
    (
        Product(
            Zip(Points(u'a', [1, 2, 3]), Points(u'b', [4, 5, 6])),
            Linspace(u'c', 0, 1, 5),
        ),
        Product(
            Zip(Points(u'a', [1, 2, 3]), Points(u'b', [4, 5, 6])),
            Zip(Linspace(u'c', 0, 1, 5)),
        ),
    ),
    (
        Product(
            Zip(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3])),
            Zip(Linspace(u'c', 0, 1, 8), Points(u'd', [1, 0.5, 0.25, 0.125])),
        ),
        Product(
            Zip(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3])),
            Zip(Linspace(u'c', 0, 1, 8), Points(u'd', [1, 0.5, 0.25, 0.125])),
        ),
    ),
])
def test_sweep_to_proto(sweep, expected):
    proto = params.sweep_to_proto(sweep)
    out = params.sweep_from_proto(proto)
    assert out == expected


@pytest.mark.parametrize(u'bad_sweep', [
    Zip(Product(Linspace(u'a', 0, 10, 25), Linspace(u'b', 0, 10, 25))),
])
def test_sweep_to_proto_fail(bad_sweep):
    with pytest.raises(ValueError):
        params.sweep_to_proto(bad_sweep)
