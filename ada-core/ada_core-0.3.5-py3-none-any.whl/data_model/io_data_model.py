from schematics import Model
from ada_core.data_model.io_data_type import BasicDataType


class BinaryNumberInput(Model):
    left = BasicDataType.FLOAT.value(required=True)
    right = BasicDataType.FLOAT.value(required=True)


class BinaryTsInput(Model):
    left = BasicDataType.TIME_SERIES.value(required=True)
    right = BasicDataType.TIME_SERIES.value(required=True)


class BinaryTsNumberInput(Model):
    left = BasicDataType.FLOAT.value(required=True)
    right = BasicDataType.TIME_SERIES.value(required=True)