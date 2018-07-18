# coding=utf-8
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import absolute_import
from typing import Optional

import numpy

from openfermioncirq.optimization import (
        BlackBox,
        OptimizationAlgorithm,
        OptimizationParams,
        OptimizationResult,
        OptimizationTrialResult)


class ExampleAlgorithm(OptimizationAlgorithm):

    def optimize(self,
                 black_box,
                 initial_guess=None,
                 initial_guess_array=None
                 ):
        pass


def test_optimization_result_init():
    result = OptimizationResult(
            optimal_value=0.339,
            optimal_parameters=numpy.array([-1.899, -0.549]),
            num_evaluations=121,
            cost_spent=1.426,
            seed=77,
            status=195,
            message=u'fdjmolGSHM')
    assert result.optimal_value == 0.339
    numpy.testing.assert_allclose(result.optimal_parameters,
                                  numpy.array([-1.899, -0.549]))
    assert result.num_evaluations == 121
    assert result.cost_spent == 1.426
    assert result.seed == 77
    assert result.status == 195
    assert result.message == u'fdjmolGSHM'


def test_optimize_trial_result_init():
    result1 = OptimizationResult(
            optimal_value=5.7,
            optimal_parameters=numpy.array([1.3, 8.7]),
            num_evaluations=59,
            cost_spent=3.1,
            seed=60,
            status=54,
            message=u'ZibVTBNe8')
    result2 = OptimizationResult(
            optimal_value=4.7,
            optimal_parameters=numpy.array([1.7, 2.1]),
            num_evaluations=57,
            cost_spent=9.3,
            seed=51,
            status=32,
            message=u'cicCZ8iCg0D')
    trial = OptimizationTrialResult(
            [result1, result2],
            params=OptimizationParams(ExampleAlgorithm()))

    assert all(trial.data_frame[u'optimal_value'] == [5.7, 4.7])
    numpy.testing.assert_allclose(
            trial.data_frame[u'optimal_parameters'][0], numpy.array([1.3, 8.7]))
    numpy.testing.assert_allclose(
            trial.data_frame[u'optimal_parameters'][1], numpy.array([1.7, 2.1]))
    assert all(trial.data_frame[u'num_evaluations'] == [59, 57])
    assert all(trial.data_frame[u'cost_spent'] == [3.1, 9.3])
    assert all(trial.data_frame[u'seed'] == [60, 51])
    assert all(trial.data_frame[u'status'] == [54, 32])
    assert all(trial.data_frame[u'message'] == [u'ZibVTBNe8', u'cicCZ8iCg0D'])


def test_optimize_trial_result_data_methods():
    result1 = OptimizationResult(
            optimal_value=5.7,
            optimal_parameters=numpy.array([1.3, 8.7]),
            num_evaluations=59,
            cost_spent=3.1,
            seed=60,
            status=54,
            message=u'ZibVTBNe8')
    result2 = OptimizationResult(
            optimal_value=4.7,
            optimal_parameters=numpy.array([1.7, 2.1]),
            num_evaluations=57,
            cost_spent=9.3,
            seed=51,
            status=32,
            message=u'cicCZ8iCg0D')
    trial = OptimizationTrialResult(
            [result1, result2],
            params=OptimizationParams(ExampleAlgorithm()))

    assert trial.repetitions == 2
    assert trial.optimal_value == 4.7
    numpy.testing.assert_allclose(trial.optimal_parameters,
                                  numpy.array([1.7, 2.1]))
    assert trial.optimal_value_quantile() == 5.2
    assert trial.num_evaluations_quantile() == 58
    assert trial.cost_spent_quantile() == 6.2
