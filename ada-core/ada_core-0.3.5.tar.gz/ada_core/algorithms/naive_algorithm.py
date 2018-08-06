from ada_core.algorithms import Algorithm
from ada_core.data_model.io_data_type import AlgorithmIODataType


class NumNaiveAlgorithm(Algorithm):

    def __init__(self):
        super(NumNaiveAlgorithm, self).__init__(self.__class__.__name__)
        # self.name = 'naive'
        # self.input_type = AlgorithmIODataType.FLOAT.value
        # self.output_type = AlgorithmIODataType.FLOAT.value

    def _run_algorithm(self, input_value):
        return input_value


class TsNaiveAlgorithm(Algorithm):

    def __init__(self):
        super(TsNaiveAlgorithm, self).__init__(self.__class__.__name__)
        # self.name = 'naive'
        # self.input_type = AlgorithmIODataType.TIME_SERIES.value
        # self.output_type = AlgorithmIODataType.TIME_SERIES.value

    def _run_algorithm(self, input_value):
        return input_value


class EntryNaiveAlgorithm(Algorithm):

    def __init__(self):
        super(EntryNaiveAlgorithm, self).__init__(self.__class__.__name__)
        # self.name = 'naive'
        # self.input_type = AlgorithmIODataType.ENTRY.value
        # self.output_type = AlgorithmIODataType.ENTRY.value

    def _run_algorithm(self, input_value):
        return input_value