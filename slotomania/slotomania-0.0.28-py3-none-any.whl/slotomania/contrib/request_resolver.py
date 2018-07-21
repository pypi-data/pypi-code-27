from enum import Enum, auto
from typing import ClassVar, Callable, Type

from marshmallow import Schema, class_registry
from slotomania.core import Sloto

from slotomania.exceptions import BadResolver
from slotomania.instructor import Instruction, Operation
from slotomania.contrib.slots import AuthenticateUserRequest


class RequestResolver:
    # data: MyDataType
    resolve: Callable
    pre_action: ClassVar[str] = ""
    callback: ClassVar[str] = ""
    use_jwt_authentication: ClassVar[bool] = True

    def __init__(self, request, data: dict) -> None:
        self.request = request
        self._data = data
        sloto_klass = self.get_data_type()
        # Validate and create sloto data
        self.validate()
        self.data = sloto_klass.sloto_from_dict(self.validated_data)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "resolve"):
            assert cls.__annotations__.get(
                "data"
            ), f"{cls} cannot define 'resovle' without annotating 'data'"
            if not cls.resolve.__annotations__:
                raise BadResolver(
                    f"{cls} must annotate resolve method if defined"
                )

    def validate(self) -> None:
        schema = self.get_schema()
        self.validated_data = schema.load(self.request.data)

    @classmethod
    def get_data_type(cls) -> Type[Sloto]:
        return cls.__annotations__["data"]

    @classmethod
    def get_schema(cls) -> Schema:
        return class_registry.get_class(cls.get_data_type().__name__)()

    def authenticate(self) -> None:
        if not self.use_jwt_authentication:
            return

        from .jwt_auth import authenticate_request
        authenticate_request(self.request)


class EntityTypes(Enum):
    jwt_auth_token = auto()


class AuthenticateUser(RequestResolver):
    """Login and InitApp."""
    data: AuthenticateUserRequest
    use_jwt_authentication = False

    def resolve(self) -> Instruction:
        from django.contrib.auth import authenticate, login
        from .jwt_auth import jwt_encode_handler, jwt_payload_handler

        username = self.data.username
        password = self.data.password
        user = authenticate(username=username, password=password)

        if user:
            login(self.request, user)

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            # init_app = InitApp(request=self.request, data=self.request.data)
            # response = init_app.resolve()
            # response.operations.append(
            #     Operation(
            #         verb=Verbs.OVERWRITE,
            #         entity_type=EntityTypes.jwt_auth_token,
            #         target_value=token
            #     )
            # )
            return Instruction(
                [Operation.OVERWRITE(EntityTypes.jwt_auth_token, token)]
            )

        return Instruction(operations=[], errors='bad credential')
