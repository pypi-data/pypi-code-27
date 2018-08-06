"""
Author: qiacai
"""


from schematics.types import StringType, FloatType, DateTimeType, IntType, NumberType, BooleanType, BaseType, ModelType
from schematics.exceptions import ConversionError, BaseError, CompoundError, ValidationError, DataError
from collections import Mapping
from enum import Enum, unique

from ada_core.data_model.entry import Entry
from ada_core.data_model.time_series import TimeSeries


class EntryType(BaseType):

    primitive_type = dict
    native_type = Entry

    def to_native(self, value, context=None):

        if hasattr(value, "timestamp") and hasattr(value, "value"):
            try:
                data = Entry(int(value.timestamp), float(value.value))
            except (BaseError, ValueError):
                raise ConversionError('timestamp could not convert to int or value could not convert to float')

        elif isinstance(value, tuple):
            if len(value) != 2:
                raise ConversionError("The input tuple should only have 2 elements")
            else:
                try:
                    data = Entry(int(value[0]), float(value[1]))
                except (BaseError, ValueError):
                    raise ConversionError('timestamp could not convert to int or value could not convert to float')

        elif isinstance(value, Mapping):
            if len(value) != 2:
                raise ConversionError("The input dict should only have 2 elements")
            elif not value.get("timestamp") or not value.get("value"):
                raise ConversionError("the input dict should have key 'timestamp' and 'value'")
            else:
                try:
                    data = Entry(int(value.get("timestamp")), float(value.get("value")))
                except (BaseError, ValueError):
                    raise ConversionError('timestamp could not convert to int or value could not convert to float')
        else:
            raise ConversionError('the input could be tuple, dict or other object having attributes: timestamp and value')

        return data

    def to_primitive(self, value, context=None):

        data = self.to_native(value)
        return {"timestamp": data.timestamp, "value": data.value}


class TimeSeriesType(BaseType):

    primitive_type = dict
    native_type = TimeSeries

    def to_native(self, value, context=None):

        if not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used in a TimeSeriesType')

        data = TimeSeries()
        errors = {}
        for k in sorted(value.keys()):
            try:
                data[int(k)] = float(value.get(k))
            except (BaseError, ValueError) as exc:
                errors[k] = exc
        if errors:
            raise CompoundError(errors)
        return data

    def to_primitive(self, value, context=None):

        if not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used in a TimeSeriesType')

        data = {}
        errors = {}

        for k in sorted(value.keys()):
            try:
                data[int(k)] = float(value.get(k))
            except (BaseError, ValueError) as exc:
                errors[k] = exc
        if errors:
            raise CompoundError(errors)
        return data


try:

    # @unique
    class BasicDataType(Enum):

        STR = StringType
        FLOAT = FloatType
        INT = IntType
        BOOL = BooleanType
        TIMESTAMP = IntType
        ENTRY = EntryType
        TIME_SERIES = TimeSeriesType

        @classmethod
        def hasType(cls, value):
            return any(value == item.value for item in cls)

        @classmethod
        def hasTypeName(cls, name):
            return any(name == item.name for item in cls)

        @classmethod
        def getType(cls, name):
            nameList = [item.name for item in AlgorithmIODataType]
            valueList = [item.value for item in cls]
            if name in nameList:
                return valueList[nameList.index()]
            else:
                return None

except ValueError as e:
    print(e)

from ada_core.data_model.io_data_model import *


class BinaryNumberInputType(BaseType):

    primitive_type = dict
    native_type = BinaryNumberInput

    def to_native(self, value, context=None):

        if isinstance(value, BinaryNumberInput):
            try:
                value.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryNumberInputType: {}'.format(exp))
            return value

        elif not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used in a BinaryNumberInputType')

        else:
            data_model = BinaryNumberInput(value)
            try:
                data_model.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryNumberInputType: {}'.format(exp))
            return data_model

    def to_primitive(self, value, context=None):

        if isinstance(value, BinaryNumberInput):
            try:
                value.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryNumberInputType: {}'.format(exp))
            return value.to_primitive()

        elif not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used in a BinaryNumberInputType')

        else:
            data_model = BinaryNumberInput(value)
            try:
                data_model.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryNumberInputType: {}'.format(exp))
            return data_model.to_primitive()


class BinaryTsInputType(BaseType):

    primitive_type = dict
    native_type = BinaryTsInput

    def to_native(self, value, context=None):

        if isinstance(value, BinaryTsInput):
            try:
                value.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryTsInput: {}'.format(exp))
            return value

        elif not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used in a BinaryTsInputType')

        else:
            data_model = BinaryTsInput(value)
            try:
                data_model.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryTsInputType: {}'.format(exp))
            return data_model

    def to_primitive(self, value, context=None):

        if isinstance(value, BinaryTsInput):
            try:
                value.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryTsInput: {}'.format(exp))
            return value.to_primitive()

        elif not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used in a BinaryTsInputType')

        else:
            data_model = BinaryTsInput(value)
            try:
                data_model.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryTsInputType: {}'.format(exp))
            return data_model.to_primitive()


class BinaryTsNumberInputType(BaseType):

    primitive_type = dict
    native_type = BinaryTsNumberInput

    def to_native(self, value, context=None):

        if isinstance(value, BinaryTsNumberInput):
            try:
                value.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryTsInput: {}'.format(exp))
            return value

        elif not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used in a BinaryTsNumberInputType')

        else:
            data_model = BinaryTsNumberInput(value)
            try:
                data_model.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryTsNumberInputType: {}'.format(exp))
            return data_model

    def to_primitive(self, value, context=None):

        if isinstance(value, BinaryTsNumberInput):
            try:
                value.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryTsInput: {}'.format(exp))
            return value.to_primitive()

        elif not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used in a BinaryTsNumberInputType')

        else:
            data_model = BinaryTsNumberInput(value)
            try:
                data_model.validate()
            except (DataError, ConversionError) as exp:
                raise ConversionError('Not validate BinaryTsNumberInputType: {}'.format(exp))
            return data_model.to_primitive()

try:
    # @unique
    class AlgorithmIODataType(Enum):

        STR = BasicDataType.STR.value
        FLOAT = BasicDataType.FLOAT.value
        INT = BasicDataType.INT.value
        BOOL = BasicDataType.BOOL.value
        TIMESTAMP = BasicDataType.TIMESTAMP.value
        ENTRY = BasicDataType.ENTRY.value
        TIME_SERIES = BasicDataType.TIME_SERIES.value
        BINARY_NUMBER_INPUT = BinaryNumberInputType
        BINARY_TS_INPUT = BinaryTsInputType
        BINARY_TS_NUMBER_INPUT = BinaryTsNumberInputType

        @classmethod
        def hasType(cls, value):
            return any(value == item.value for item in cls)

        @classmethod
        def hasTypeName(cls, name):
            return any(name == item.name for item in cls)

        @classmethod
        def getAllTypeName(cls):
            return [item.name for item in cls]

        @classmethod
        def getAllType(cls):
            return [item.value for item in cls]

        @classmethod
        def getType(cls, name):
            nameList = [item.name for item in cls]
            valueList = [item.value for item in cls]
            if name in nameList:
                return valueList[nameList.index(name)]
            else:
                return None

        @classmethod
        def getTypeName(cls, value):
            nameList = [item.name for item in cls]
            valueList = [item.value for item in cls]
            if value in valueList:
                return nameList[valueList.index(value)]
            else:
                return None


        @classmethod
        def deduceType(cls, input_value):

            type_validate = False
            input_type = None
            try:
                if not type_validate:
                    boolType = AlgorithmIODataType.BOOL.value()
                    boolType.validate(input_value)
                    type_validate = True
                    return AlgorithmIODataType.BOOL.value
            except BaseError:
                type_validate = False

            try:
                if not type_validate:
                    floatType = AlgorithmIODataType.FLOAT.value()
                    floatType.validate(input_value)
                    type_validate = True
                    return AlgorithmIODataType.FLOAT.value
            except BaseError:
                type_validate = False

            try:
                if not type_validate:
                    tsType = AlgorithmIODataType.TIME_SERIES.value()
                    tsType.validate(input_value)
                    type_validate = True
                    return AlgorithmIODataType.TIME_SERIES.value
            except BaseError:
                type_validate = False

            try:
                if not type_validate:
                    binaryNumType = AlgorithmIODataType.BINARY_NUMBER_INPUT.value()
                    binaryNumType.validate(input_value)
                    type_validate = True
                    return AlgorithmIODataType.BINARY_NUMBER_INPUT.value
            except BaseError:
                type_validate = False

            try:
                if not type_validate:
                    binaryTsNumType = AlgorithmIODataType.BINARY_TS_NUMBER_INPUT.value()
                    binaryTsNumType.validate(input_value)
                    type_validate = True
                    return AlgorithmIODataType.BINARY_TS_NUMBER_INPUT.value
            except BaseError:
                type_validate = False

            try:
                if not type_validate:
                    binaryTsType = AlgorithmIODataType.BINARY_TS_INPUT.value()
                    binaryTsType.validate(input_value)
                    type_validate = True
                    return AlgorithmIODataType.BINARY_TS_INPUT.value
            except BaseError:
                type_validate = False

            return input_type


except ValueError as e:
    print(e)