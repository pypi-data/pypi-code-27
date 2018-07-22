import datetime
from typing import Optional
from unittest import TestCase
from dataclasses import dataclass, is_dataclass, asdict
from slotomania.contrib.dataclass_converter import (
    contracts_to_typescript,
    Contract,
)


@dataclass
class Person(Contract):
    name: str
    gender: bool
    birth_date: datetime.datetime
    spouse: Optional["Person"] = None


class DataclassConverterTestCase(TestCase):
    def test_dataclass_converter(self) -> None:
        assert is_dataclass(Person)
        man = Person("Bond", True, datetime.datetime.utcnow())
        woman = Person("Girl", True, datetime.datetime.utcnow(), spouse=man)
        assert is_dataclass(man) and is_dataclass(woman)
        assert contracts_to_typescript(
            dataclasses=[Person], redux_actions=[]
        ) == ""
