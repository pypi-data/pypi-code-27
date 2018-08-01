from typing import List, Union

import jsonpath_rw
from typeguard import check_type


class Attribute:
    def __init__(self, path: str):
        self._path = path
        self._expr = jsonpath_rw.parse(self._path)

    def __get__(self, obj, obj_type=None):
        return self._format(
            result=self._expr.find(obj.raw),
            path=self._path,
            strict_validation=obj.Meta.strict_validation)

    @staticmethod
    def _format(result: list, path: str, strict_validation: bool):
        raise NotImplemented


class StringAttribute(Attribute):
    @staticmethod
    def _format(result: list, path: str, strict_validation: bool) -> str:
        formatted = result[0].value

        if strict_validation:
            check_type(path, formatted, str, memo=None)

        return formatted


class StringListAttribute(Attribute):
    @staticmethod
    def _format(result: list, path: str, strict_validation: bool) -> List[str]:
        formatted = list(map(lambda x: x.value, result))

        if strict_validation:
            check_type(path, formatted, List[str], memo=None)

        return list(map(lambda x: x.value, result))


class NumberAttribute(Attribute):
    @staticmethod
    def _format(result: list, path: str, strict_validation: bool) -> Union[int, float]:
        formatted = result[0].value

        if strict_validation:
            check_type(path, formatted, Union[int, float], memo=None)

        return formatted


class NumberListAttribute(Attribute):
    @staticmethod
    def _format(result: list, path: str, strict_validation: bool) -> List[Union[int, float]]:
        formatted = list(map(lambda x: x.value, result))

        if strict_validation:
            check_type(path, formatted, List[Union[int, float]], memo=None)

        return formatted


class BooleanAttribute(Attribute):
    @staticmethod
    def _format(result: list, path: str, strict_validation: bool) -> bool:
        formatted = result[0].value

        if strict_validation:
            check_type(path, formatted, bool, memo=None)

        return formatted


class BooleanListAttribute(Attribute):
    @staticmethod
    def _format(result: list, path: str, strict_validation: bool) -> List[bool]:
        formatted = list(map(lambda x: x.value, result))

        if strict_validation:
            check_type(path, formatted, List[bool], memo=None)

        return formatted


class ListAttribute(Attribute):
    @staticmethod
    def _format(result: list, path: str, strict_validation: bool) -> list:
        formatted = list(map(lambda x: x.value, result))

        if strict_validation:
            check_type(path, formatted, list, memo=None)

        return formatted


class ObjectAttribute(Attribute):
    @staticmethod
    def _format(result: list, path: str, strict_validation: bool) -> dict:
        formatted = dict([(k, v) for k, v in result[0].value.items()])

        if strict_validation:
            check_type(path, formatted, dict, memo=None)

        return formatted
