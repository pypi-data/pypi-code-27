"""
Author: qiacai
"""

import pytz

from schematics.models import Model
from schematics.types import StringType, ModelType
from schematics.exceptions import ConversionError, BaseError, CompoundError, ValidationError

from ada_core import exceptions, utils, constants
from ada_core.data_model.io_data_type import AlgorithmIODataType
from ada_core.algorithms import *


__all__ = ['NumNaiveAlgorithmMeta', 'TsNaiveAlgorithmMeta', 'EntryNaiveAlgorithmMeta',
           'EqualBinaryJudgeAlgorithmMeta', 'GreaterThanJudgeAlgorithmMeta',
           'GreaterThanOrEqualBinaryJudgeAlgorithmMeta', 'GreaterThanOrEqualBinaryJudgeAlgorithmMeta',
           'GreaterThanOrEqualBinaryJudgeAlgorithmMeta', 'LessThanBinaryJudgeAlgorithmMeta',
           'LessThanOrEqualBinaryJudgeAlgorithmMeta',
           'MeanAlgorithmMeta', 'MedianAlgorithmMeta', 'MaxAlgorithmMeta', 'MinAlgorithmMeta', 'CushionAlgorithmMeta',
           'PercentileAlgorithmMeta', 'StdAlgorithmMeta', 'MadAlgorithmMeta', 'CountAlgorithmMeta', 'SumAlgorithmMeta',
           'ValueScaleAlgorithmMeta', 'TimeOffsetAlgorithmMeta', 'StandardNormalizationAlgorithmMeta',
           'ScaleNormalizationAlgorithmMeta', 'ExponentialSmoothAlgorithmMeta', 'SeasonalDecomposeAlgorithmMeta',
           'EntryHardThresholdAlgorithmMeta', 'TsHardThresholdAlgorithmMeta', 'NumHardThresholdAlgorithmMeta',
           'SoftThresholdAlgorithmMeta', 'CushionThresholdAlgorithmMeta'
           ]


class NumNaiveAlgorithmMeta(Model):
    alg_name = 'naive'
    input_value = AlgorithmIODataType.FLOAT.value(required=True)
    output_value = AlgorithmIODataType.FLOAT.value()
    alg_cls = naive_algorithm.NumNaiveAlgorithm


class TsNaiveAlgorithmMeta(Model):
    alg_name = 'naive'
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.TIME_SERIES.value()
    alg_cls = naive_algorithm.TsNaiveAlgorithm


class EntryNaiveAlgorithmMeta(Model):
    alg_name = 'naive'
    input_value = AlgorithmIODataType.ENTRY.value(required=True)
    output_value = AlgorithmIODataType.ENTRY.value()
    alg_cls = naive_algorithm.EntryNaiveAlgorithm


class BaseBinaryNum1NumJudgeAlgorithmMeta(Model):
    alg_name = 'base_binary_judge'
    input_value = AlgorithmIODataType.BINARY_NUMBER_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_cls = binary_num1num_judge_algorithms.BaseBinaryNum1NumJudgeAlgorithm


class EqualBinaryJudgeAlgorithmMeta(BaseBinaryNum1NumJudgeAlgorithmMeta):
    alg_name = '=='
    alg_cls = binary_num1num_judge_algorithms.EqualBinaryJudgeAlgorithm


class GreaterThanJudgeAlgorithmMeta(BaseBinaryNum1NumJudgeAlgorithmMeta):
    alg_name = '>'
    alg_cls = binary_num1num_judge_algorithms.GreaterThanBinaryJudgeAlgorithm


class GreaterThanOrEqualBinaryJudgeAlgorithmMeta(BaseBinaryNum1NumJudgeAlgorithmMeta):
    alg_name = '>='
    alg_cls = binary_num1num_judge_algorithms.GreaterThanOrEqualBinaryJudgeAlgorithm


class LessThanBinaryJudgeAlgorithmMeta(BaseBinaryNum1NumJudgeAlgorithmMeta):
    alg_name = '<'
    alg_cls = binary_num1num_judge_algorithms.LessThanBinaryJudgeAlgorithm


class LessThanOrEqualBinaryJudgeAlgorithmMeta(BaseBinaryNum1NumJudgeAlgorithmMeta):
    alg_name = '<='
    alg_cls = binary_num1num_judge_algorithms.LessThanOrEqualBinaryJudgeAlgorithm


class BaseUnaryTs2NumCalAlgorithmMeta(Model):
    alg_name = 'base_unary_ts2num_calculate'
    alg_cls = unary_ts2num_calculate_algorithms.BaseUnaryTs2NumCalAlgorithm
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.FLOAT.value()


class MeanAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'mean'
    alg_cls = unary_ts2num_calculate_algorithms.Mean
    default = AlgorithmIODataType.FLOAT.value()


class MedianAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'median'
    alg_cls = unary_ts2num_calculate_algorithms.Median
    default = AlgorithmIODataType.FLOAT.value()


class MaxAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'max'
    alg_cls = unary_ts2num_calculate_algorithms.Max
    default = AlgorithmIODataType.FLOAT.value()


class MinAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'min'
    alg_cls = unary_ts2num_calculate_algorithms.Min
    default = AlgorithmIODataType.FLOAT.value()


class PercentileAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'percentile'
    alg_cls = unary_ts2num_calculate_algorithms.Percentile
    default = AlgorithmIODataType.FLOAT.value()
    percentile = AlgorithmIODataType.INT.value(min_value=0, max_value=100, default=constants.ALGORITHM_DEFAULT_CALCULATOR_PERCENTILE_PERCENTILE)


class StdAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'std'
    alg_cls = unary_ts2num_calculate_algorithms.Std
    default = AlgorithmIODataType.FLOAT.value()


class MadAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'mad'
    alg_cls = unary_ts2num_calculate_algorithms.Mad
    default = AlgorithmIODataType.FLOAT.value()


# Not Fully Implemented
class CushionAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'cushion'
    alg_cls = unary_ts2num_calculate_algorithms.Cushion
    default = AlgorithmIODataType.FLOAT.value()
    upper_percentile = AlgorithmIODataType.INT.value(min_value=0, max_value=100, default=constants.ALGORITHM_DEFAULT_CALCULATOR_CUSHION_UPPER_PERCENTILE)
    lower_percentile = AlgorithmIODataType.INT.value(min_value=0, max_value=100, default=constants.ALGORITHM_DEFAULT_CALCULATOR_CUSHION_LOWER_PERCENTILE)
    is_upper = AlgorithmIODataType.BOOL.value(default=constants.ALGORITHM_DEFAULT_CALCULATOR_CUSHION_IS_UPPER)


class CountAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'count'
    alg_cls = unary_ts2num_calculate_algorithms.Count
    input_value = AlgorithmIODataType.INT.value()
    default = AlgorithmIODataType.INT.value()


class SumAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'sum'
    alg_cls = unary_ts2num_calculate_algorithms.Sum
    default = AlgorithmIODataType.FLOAT.value()


class BaseBinaryTs1Num2TsCalAlgorithmMeta(Model):
    alg_name = 'base_binary_ts1num2ts_calculate'
    input_value = AlgorithmIODataType.BINARY_TS_NUMBER_INPUT.value(required=True)
    output_value = AlgorithmIODataType.TIME_SERIES.value()
    alg_cls = binary_ts1num2ts_calculate_algorithms.BaseBinaryTs1Num2TsCalAlgorithm


class ValueScaleAlgorithmMeta(BaseBinaryTs1Num2TsCalAlgorithmMeta):
    alg_name = 'value_scale'
    alg_cls = binary_ts1num2ts_calculate_algorithms.ValueScale
    operator = StringType(choices=['+', '-', '*', '/'], default=constants.ALGORITHM_DEFAULT_CALCULATOR_VALUE_SCALE_OPERATOR)


class BaseUnaryTs2TsCalAlgorithmMeta(Model):
    alg_name = 'base_unary_ts2ts_calculate'
    alg_cls = unary_ts2ts_calculate_algorithms.BaseUnaryTs2TsCalAlgorithm
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.TIME_SERIES.value()


class TimeOffsetAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'time_offset'
    alg_cls = unary_ts2ts_calculate_algorithms.TimeOffset
    offset = AlgorithmIODataType.INT.value(default=constants.ALGORITHM_DEFAULT_CALCULATOR_TIME_OFFSET_OFFSET)


class StandardNormalizationAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'standard_normalization'
    alg_cls = unary_ts2ts_calculate_algorithms.StandardNormalization


class ScaleNormalizationAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'scale_normalization'
    alg_cls = unary_ts2ts_calculate_algorithms.StandardNormalization


class ExponentialSmoothAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'exponential_smooth'
    alg_cls = unary_ts2ts_calculate_algorithms.ExponentialSmooth
    smoothing_factor = AlgorithmIODataType.FLOAT.value(min_value=0, max_value=1, default=constants.ALGORITHM_DEFAULT_CALCULATOR_EXPONENTIAL_SMOOTH_SMOOTHING_FACTOR)


class SeasonalDecomposeAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'seasonal_decompose'
    alg_cls = unary_ts2ts_calculate_algorithms.SeasonalDecompose
    freq = AlgorithmIODataType.INT.value(min_value=0, default=constants.ALGORITHM_DEFAULT_CALCULATOR_SEASONAL_DECOMPOSE_FREQ)
    trend_only = AlgorithmIODataType.BOOL.value(default=constants.ALGORITHM_DEFAULT_CALCULATOR_SEASONAL_DECOMPOSE_TREND_ONLY)
    is_fillna = AlgorithmIODataType.BOOL.value(default=constants.ALGORITHM_DEFAULT_CALCULATOR_SEASONAL_DECOMPOSE_FILLNA)


# Not Fully Implemented
class EntryHardThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.ENTRY.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'hard_threshold'
    alg_cls = unary_judge_algorithms.HardThreshold
    operator = StringType(choices=['>', '>=', '<', '<=', '=='], default=constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_OPERATOR)
    threshold = AlgorithmIODataType.FLOAT.value(required=True, default=constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_THRESHOLD)


class TsHardThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'hard_threshold'
    alg_cls = unary_judge_algorithms.HardThreshold
    operator = StringType(choices=['>', '>=', '<', '<=', '=='], default=constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_OPERATOR)
    threshold = AlgorithmIODataType.FLOAT.value(required=True, default=constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_THRESHOLD)
    local_window = StringType(default=constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_LOCAL_WINDOW, regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    timezone = StringType(choices=pytz.all_timezones, default=constants.ALGORITHM_DEFAULT_TIMEZONE)


class NumHardThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.FLOAT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'hard_threshold'
    alg_cls = unary_judge_algorithms.HardThreshold
    operator = StringType(choices=['>', '>=', '<', '<=', '=='], default=constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_OPERATOR)
    threshold = AlgorithmIODataType.FLOAT.value(required=True, default=constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_THRESHOLD)


class SoftThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'soft_threshold'
    alg_cls = unary_judge_algorithms.SoftThreshold
    operator = StringType(choices=['>', '>=', '<', '<='], default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_OPERATOR)
    local_window = StringType(default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_LOCAL_WINDOW, regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    lag_window = StringType(default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_LAG_WINDOW, regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    benchmark_method = StringType(choices=['mean', 'exponential', 'median'], default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_BENCHMARK_METHOD)
    factor = AlgorithmIODataType.FLOAT.value(required=True, default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_FACTOR, min_value=0)
    bound_method = StringType(choices=['hard', 'std', 'mad', 'ratio'], default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_BOUND_METHOD)
    timezone = StringType(choices=pytz.all_timezones, default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_TIMEZONE)


class CushionThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'cushion_threshold'
    alg_cls = unary_judge_algorithms.CushionThreshold
    operator = StringType(choices=['>', '>=', '<', '<='], default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_OPERATOR)
    local_window = StringType(default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LOCAL_WINDOW,regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    lag_window = StringType(default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LAG_WINDOW, regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    benchmark_method = StringType(choices=['mean', 'exponential', 'median'], default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_BENCHMARK_METHOD)
    factor = AlgorithmIODataType.FLOAT.value(required=True, default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_FACTOR, min_value=0)
    timezone = StringType(choices=pytz.all_timezones, default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_TIMEZONE)
    upper_percentile = AlgorithmIODataType.INT.value(min_value=0, max_value=100, default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_UPPER_PERCENTILE)
    lower_percentile = AlgorithmIODataType.INT.value(min_value=0, max_value=100, default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LOWER_PERCENTILE)
    #is_upper = AlgorithmIODataType.BOOL.value(default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_IS_UPPER)