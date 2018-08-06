"""
Author: qiacai
"""

from ada_core import exceptions, constants, utils
from ada_core.algorithms import Algorithm
from ada_core.data_model.io_data_type import AlgorithmIODataType


class HardThreshold(Algorithm):
    def __init__(self):
        super(HardThreshold, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, operator=None, local_window=None, threshold=None, timezone=None):

        if threshold is None:
            threshold = constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_THRESHOLD

        if operator is None:
            operator = constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_OPERATOR

        if local_window is None:
            local_window = constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_LOCAL_WINDOW

        if timezone is None:
            timezone = constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_TIMEZONE

        from ada_core.algorithms.algorithm_factory import AlgorithmFactory
        algorithm_factory = AlgorithmFactory()
        if type(input_value) == AlgorithmIODataType.ENTRY.value.native_type:
            compare_value = input_value.value
        elif type(input_value) == AlgorithmIODataType.TIME_SERIES.value.native_type:
            mean_alg = algorithm_factory.getAlgorithm('mean', AlgorithmIODataType.TIME_SERIES.value)
            local_timestamp = utils.window2timestamp(input_value, local_window, timezone)
            local_ts = input_value.split(key=local_timestamp)
            compare_value = mean_alg.run(local_ts)
        else:
            compare_value = input_value
        if compare_value is None:
            return None
        else:
            op_input_type = AlgorithmIODataType.BINARY_NUMBER_INPUT.value()
            op_input = op_input_type.to_native({'left': compare_value, 'right': threshold})
            op_alg = algorithm_factory.getAlgorithm(operator, AlgorithmIODataType.BINARY_NUMBER_INPUT.value)
            return op_alg.run(op_input)
            #
            #
            # if operator == '>':
            #     return True if compare_value > threshold else False
            # elif operator == '>=':
            #     return True if compare_value >= threshold else False
            # elif operator == '<':
            #     return True if compare_value < threshold else False
            # elif operator == '<=':
            #     return True if compare_value <= threshold else False
            # elif operator == '==':
            #     return True if compare_value == threshold else False
            # else:
            #     return None


class SoftThreshold(Algorithm):
    def __init__(self):
        super(SoftThreshold, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value, operator=None, local_window=None, lag_window=None, benchmark_method=None,
                       bound_method=None, factor=None, timezone=None):

        if operator is None:
            operator = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_OPERATOR
        if operator in ['>', '>=']:
            sign = 1
        else:
            sign = -1


        if local_window is None:
            local_window = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_LOCAL_WINDOW

        if lag_window is None:
            lag_window = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_LAG_WINDOW

        if benchmark_method is None:
            benchmark_method = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_BENCHMARK_METHOD

        if bound_method is None:
            bound_method = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_BOUND_METHOD

        if factor is None:
            factor = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_FACTOR

        if timezone is None:
            timezone = constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_TIMEZONE

        from ada_core.algorithms.algorithm_factory import AlgorithmFactory
        algorithm_factory = AlgorithmFactory()

        mean_alg = algorithm_factory.getAlgorithm('mean', AlgorithmIODataType.TIME_SERIES.value)
        local_timestamp = utils.window2timestamp(input_value, local_window, timezone)
        local_ts = input_value.split(key=local_timestamp, direct=True)
        compare_value = mean_alg.run(local_ts)

        benchmark_timestamp = utils.window2timestamp(input_value, lag_window, timezone)
        bnckmk_alg = algorithm_factory.getAlgorithm(benchmark_method, AlgorithmIODataType.TIME_SERIES.value)
        bnckmk_ts = input_value.split(key=benchmark_timestamp)
        bnckmk_value = bnckmk_alg.run(bnckmk_ts)

        if bound_method == 'hard':
            bound_value = sign*factor + bnckmk_value
        elif bound_method == 'ratio':
            bound_value = bnckmk_value * (1 + sign*factor/100.0)
        else:
            bound_alg = algorithm_factory.getAlgorithm(benchmark_method, AlgorithmIODataType.TIME_SERIES.value)
            bound_value = bound_alg.run(bnckmk_ts)
            bound_value = sign*factor * bound_value + bnckmk_value

        if compare_value is None or bound_value is None:
            return None
        else:
            op_input_type = AlgorithmIODataType.BINARY_NUMBER_INPUT.value()
            op_input = op_input_type.to_native({'left': compare_value, 'right': bound_value})
            #op_input = AlgorithmIODataType.BINARY_NUMBER_INPUT.value({'left': compare_value, 'right': bound_value})
            op_alg = algorithm_factory.getAlgorithm(operator, AlgorithmIODataType.BINARY_NUMBER_INPUT.value)
            return op_alg.run(op_input)

            # if operator == '>':
            #     return True if compare_value > bound_value else False
            # elif operator == '>=':
            #     return True if compare_value >= bound_value else False
            # elif operator == '<':
            #     return True if compare_value < bound_value else False
            # elif operator == '<=':
            #     return True if compare_value <= bound_value else False
            # elif operator == '==':
            #     return True if compare_value == bound_value else False
            # else:
            #     return None


class CushionThreshold(SoftThreshold):
    def _run_algorithm(self, input_value, operator=None, local_window=None, lag_window=None, benchmark_method=None,
                       factor=None, timezone=None, upper_percentile=None, lower_percentile=None):

        if upper_percentile is None:
            upper_percentile = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_UPPER_PERCENTILE

        if lower_percentile is None:
            lower_percentile = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LOWER_PERCENTILE

        # if is_upper is None:
        #     is_upper = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_IS_UPPER

        if operator is None:
            operator = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_OPERATOR

        if operator in ['>', '>=']:
            sign = 1
        else:
            sign = -1

        if local_window is None:
            local_window = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LOCAL_WINDOW

        if lag_window is None:
            lag_window = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LAG_WINDOW

        if benchmark_method is None:
            benchmark_method = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_BENCHMARK_METHOD

        if factor is None:
            factor = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_FACTOR

        if timezone is None:
            timezone = constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_TIMEZONE

        from ada_core.algorithms.algorithm_factory import AlgorithmFactory
        algorithm_factory = AlgorithmFactory()

        mean_alg = algorithm_factory.getAlgorithm('mean', AlgorithmIODataType.TIME_SERIES.value)
        local_timestamp = utils.window2timestamp(input_value, local_window, timezone)
        local_ts = input_value.split(key=local_timestamp, direct=True)
        compare_value = mean_alg.run(local_ts)

        benchmark_timestamp = utils.window2timestamp(input_value, lag_window, timezone)
        bnckmk_alg = algorithm_factory.getAlgorithm(benchmark_method, AlgorithmIODataType.TIME_SERIES.value)
        bnckmk_ts = input_value.split(key=benchmark_timestamp)
        bnckmk_value = bnckmk_alg.run(bnckmk_ts)

        cushion_alg = algorithm_factory.getAlgorithm('cushion', AlgorithmIODataType.TIME_SERIES.value)
        cushion_value = cushion_alg.run(bnckmk_ts, is_upper=bool(sign), upper_percentile=upper_percentile, lower_percentile=lower_percentile)
        std_alg = algorithm_factory.getAlgorithm('std', AlgorithmIODataType.TIME_SERIES.value)
        std_value = std_alg.run(bnckmk_ts)
        bound_value = sign * factor * std_value * cushion_value + bnckmk_value

        if compare_value is None or bound_value is None:
            return None
        else:
            op_input_type = AlgorithmIODataType.BINARY_NUMBER_INPUT.value()
            op_input = op_input_type.to_native({'left': compare_value, 'right': bound_value})
            #op_input = AlgorithmIODataType.BINARY_NUMBER_INPUT.value({'left': compare_value, 'right': bound_value})
            op_alg = algorithm_factory.getAlgorithm(operator, AlgorithmIODataType.BINARY_NUMBER_INPUT.value)
            return op_alg.run(op_input)

            # if operator == '>':
            #     return True if compare_value > bound_value else False
            # elif operator == '>=':
            #     return True if compare_value >= bound_value else False
            # elif operator == '<':
            #     return True if compare_value < bound_value else False
            # elif operator == '<=':
            #     return True if compare_value <= bound_value else False
            # elif operator == '==':
            #     return True if compare_value == bound_value else False
            # else:
            #     return None