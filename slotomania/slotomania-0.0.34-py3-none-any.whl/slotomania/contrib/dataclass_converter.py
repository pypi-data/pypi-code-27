import datetime
from decimal import Decimal
from typing import List, Type, Dict, Union, ForwardRef  # type:ignore
from dataclasses import dataclass, Field, MISSING


def is_field_required(field: Field) -> bool:
    return field.default is MISSING


def python_type_to_typescript(python_type) -> str:
    MAP = {
        str: 'string',
        bool: 'boolean',
        int: 'number',
        Decimal: 'string',
        float: 'number',
        datetime.datetime: 'string',
        dict: '{}',
    }
    if python_type in MAP:
        return MAP[python_type]

    if getattr(python_type, "__name__", None) == "NoneType":
        return "null"

    if getattr(python_type, "__origin__", None) == Union:
        args = python_type.__args__
        return "|".join(python_type_to_typescript(arg) for arg in args)

    if isinstance(python_type, ForwardRef):
        return python_type.__forward_arg__


def field_to_typescript(field: Field) -> str:
    return python_type_to_typescript(field.type)


@dataclass
class Contract:
    @classmethod
    def get_fields(cls) -> Dict[str, Field]:
        return getattr(cls, "__dataclass_fields__")

    @classmethod
    def translate_to_typescript(cls) -> str:
        interface_body = '\n'.join(
            [
                f"  {field.name}: {field_to_typescript(field)}"
                if is_field_required(field) else
                f"  {field.name}?: {field_to_typescript(field)}"
                for name, field in cls.get_fields().items()
            ]
        )
        return 'export interface {} {{\n{}\n}}'.format(
            cls.__name__, interface_body
        )


@dataclass
class ReduxAction:
    name: str
    contract: Contract
    pre_action: str = ""
    callback: str = ""


def contracts_to_typescript(
    *,
    dataclasses: List[Type[Contract]],
    redux_actions: List[ReduxAction],
    import_plugins: bool = True,
) -> str:
    """
    Args:
        interface_schemas: A list of schemas to be converted to typescript
    interfaces.
        redux_actions: A list of ReduxAction to be converted to typescript
    creators.
    """
    blocks = import_plugins and ['import * as instructor from "./instructor"'
                                 ] or []
    for index, contract in enumerate(dataclasses):
        blocks.append(contract.translate_to_typescript())

    if redux_actions:
        # blocks.append(write_redux_actions(redux_actions))
        names = ',\n'.join([action.name for action in redux_actions])
        blocks.append(
            f"""export const SLOTO_ACTION_CREATORS = {{ {names} }}"""
        )

    return "\n\n".join(blocks)
