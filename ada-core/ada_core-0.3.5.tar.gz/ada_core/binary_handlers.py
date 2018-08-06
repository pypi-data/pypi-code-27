"""
Author: qiacai

UnaryJudger: deal with the cases where only have one input

"""
from ada_core import exceptions
from ada_core.handler import Handler
from ada_core.data_model.io_data_type import AlgorithmIODataType


class BinaryHandler(Handler):
    def __init__(self, algorithm_name, handler_input_left, handler_input_right, algorithm_input_type=None,
                 algorithm_output_type=None, params=None):
        super(BinaryHandler, self).__init__(algorithm_name=algorithm_name, algorithm_input_type=algorithm_input_type,
                                            algorithm_output_type=algorithm_output_type, params=params)
        # self._parse_handler_input(handler_input_left, handler_input_right)

    def _parse_handler_input(self, handler_input_left, handler_input_right):
        self.handler_input = {'left': handler_input_left, 'right': handler_input_right}


class BinaryTsTsHandler(BinaryHandler):
    def __init__(self, algorithm_name, ts1, ts2, algorithm_input_type=None, algorithm_output_type=None, params=None):
        super(BinaryTsTsHandler, self).__init__(algorithm_name=algorithm_name, handler_input_left=ts1,
                                                handler_input_right=ts2, algorithm_input_type=algorithm_input_type,
                                                algorithm_output_type=algorithm_output_type, params=params)

    def _parse(self):
        super(BinaryTsTsHandler, self)._parse()

        if self.algorithm_input_type != AlgorithmIODataType.BINARY_TS_INPUT.value:
            raise exceptions.ParametersNotPassed(
                'the algorithm_input_type is not Bool, please change to other handlers')


# class BinaryTsTsJudger(BinaryTsTsHandler):
#     def _parse(self):
#         super(BinaryTsTsJudger, self)._parse()
#
#         if self.algorithm_output_type != AlgorithmIODataType.BOOL.value:
#             raise exceptions.ParametersNotPassed(
#                 'the algorithm_output_type is not Bool, please change to other handlers')


class BinaryTsNumHandler(BinaryHandler):
    def __init__(self, algorithm_name, ts, num, algorithm_input_type=None, algorithm_output_type=None, params=None):
        super(BinaryTsNumHandler, self).__init__(algorithm_name=algorithm_name, handler_input_left=ts,
                                                 handler_input_right=num, algorithm_input_type=algorithm_input_type,
                                                 algorithm_output_type=algorithm_output_type, params=params)

    def _parse(self):
        super(BinaryTsNumHandler, self)._parse()

        if self.algorithm_input_type != AlgorithmIODataType.BINARY_TS_NUMBER_INPUT.value:
            raise exceptions.ParametersNotPassed(
                'the algorithm_input_type is not Bool, please change to other handlers')


# class BinaryTsNumJudger(BinaryTsTsHandler):
#     def _parse(self):
#         super(BinaryTsNumJudger, self)._parse()
#
#         if self.algorithm_output_type != AlgorithmIODataType.BOOL.value:
#             raise exceptions.ParametersNotPassed(
#                 'the algorithm_output_type is not Bool, please change to other handlers')


class BinaryNumNumHandler(BinaryHandler):
    def __init__(self, algorithm_name, num1, num2, algorithm_input_type=None, algorithm_output_type=None, params=None):
        super(BinaryNumNumHandler, self).__init__(algorithm_name=algorithm_name, handler_input_left=num1,
                                                  handler_input_right=num2, algorithm_input_type=algorithm_input_type,
                                                  algorithm_output_type=algorithm_output_type, params=params)

    def _parse(self):
        super(BinaryNumNumHandler, self)._parse()

        if self.algorithm_input_type != AlgorithmIODataType.BINARY_TS_INPUT.value:
            raise exceptions.ParametersNotPassed(
                'the algorithm_input_type is not Bool, please change to other handlers')


# class BinaryNumNumJudger(BinaryNumNumHandler):
#     def _parse_input(self):
#         super(BinaryNumNumJudger, self)._parse()
#
#         if self.algorithm_output_type != AlgorithmIODataType.BOOL.value:
#             raise exceptions.ParametersNotPassed(
#                 'the algorithm_output_type is not Bool, please change to other handlers')
