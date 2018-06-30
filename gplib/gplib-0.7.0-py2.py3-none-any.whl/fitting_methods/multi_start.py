# -*- coding: utf-8 -*-
#
#    Copyright 2018 Ibai Roman
#
#    This file is part of GPlib.
#
#    GPlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GPlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GPlib. If not, see <http://www.gnu.org/licenses/>.

import time

import numpy as np
import scipy.optimize as spo

from .fitting_method import FittingMethod


class MultiStart(FittingMethod):
    """

    """

    def __init__(self, measurement, ls_method="Powell",
                 max_fun_call=5000, max_ls_fun_call=2000):

        if ls_method in ["Newton-CG", "dogleg", "trust-ncg"]:
            raise NotImplementedError("Hessian not implemented for {}".format(
                ls_method
            ))
        self.grad_needed = ls_method in [
            "CG", "BFGS", "Newton-CG", "L-BFGS-B",
            "TNC", "SLSQP", "dogleg", "trust-ncg"
        ]
        self.bounded_search = ls_method in [
            "L-BFGS-B", "TNC", "SLSQP"
        ]
        self.max_fun_call = max_fun_call
        self.max_ls_fun_call = max_ls_fun_call
        self.ls_method = ls_method
        self.measurement = measurement

    def fit(self, model, train_set, test_set=None):
        """
        Optimize Hyperparameters

        :param model:
        :type model:
        :param train_set:
        :type train_set:
        :param test_set:
        :type test_set:
        :return:
        :rtype:
        """

        def measurement_wrapper(mod_params):
            """
            measurement wrapper to optimize hyperparameters

            :param mod_params:
            :type mod_params:
            :return:
            :rtype:
            """
            current['fun_call'] += 1
            current['ls_fun_call'] += 1

            assert current['fun_call'] < self.max_fun_call,\
                "Funcall limit reached"
            assert current['ls_fun_call'] < self.max_ls_fun_call,\
                "LS Funcall limit reached"

            gradient = np.random.uniform(-1, 1, len(mod_params))

            value = np.inf

            try:
                model.set_param_values(mod_params, trans=True)
                result = self.measurement.measure(
                    model=model,
                    train_set=train_set,
                    test_set=test_set,
                    grad_needed=self.grad_needed
                )
                if self.grad_needed:
                    value, gradient = result
                else:
                    value = result
                current['exceptions'] = 0
            except np.linalg.linalg.LinAlgError as ex:
                raise ex
            except AssertionError as ex:
                if current['exceptions'] > 5:
                    raise ex
                current['exceptions'] += 1

            if value < current['value']:
                current['value'] = value
                current['params'] = model.get_param_values()

            if self.grad_needed:
                return value, gradient

            return value

        ls_method = self.ls_method
        if self.ls_method == "Powell":
            def mod_powell(fun, x0, args=(), **kwargs):
                """

                :return:
                :rtype:
                """
                rand_perm = np.random.permutation(len(x0))
                direc = np.eye(len(x0))
                direc = direc[rand_perm]

                spo.fmin_powell(fun, x0, args, disp=kwargs['disp'], direc=direc)
            ls_method = mod_powell

        bounds = None
        if self.bounded_search:
            bounds = model.get_param_bounds(trans=True)

        start = time.time()
        fun_calls = 0
        improvements = 0
        restarts = 0
        
        best = {
            'params': None,
            'value': np.inf,
            'ls_fun_call': 0,
            'restart': 0,
            'fun_call': 0
        }

        while fun_calls < self.max_fun_call:
            # run optimization
            current = {
                'params': None,
                'value': np.inf,
                'ls_fun_call': 0,
                'exceptions': 0,
                'fun_call': fun_calls
            }
            x_0 = model.get_param_values(trans=True)
            try:
                spo.minimize(
                    measurement_wrapper,
                    x_0, method=ls_method,
                    jac=self.grad_needed, bounds=bounds,
                    options={
                        'disp': False
                    }
                )
            except (AssertionError, np.linalg.linalg.LinAlgError):
                pass

            fun_calls = current['fun_call']
            restarts += 1
            if current['value'] < best['value']:
                improvements += 1
                best['value'] = current['value']
                best['params'] = current['params']
                best['restart'] = restarts
                best['fun_call'] = fun_calls
                best['ls_fun_call'] = current['ls_fun_call']
            model.set_params_at_random(trans=True)

        end = time.time()
        
        log = {
            'fun_calls': fun_calls,
            'improvements': improvements,
            'restarts': restarts,
            'time': end - start,
            'best': best
        }

        assert best['params'], "No params were found"

        model.set_param_values(best['params'], trans=False)

        model.save_current_as_optimized()

        return log
