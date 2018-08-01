from types import LambdaType
from typing import TypeVar

__all__ = [
    'Injector'
]


T = TypeVar('T')


class Injector:

    def __init__(self):
        self._registry = {}

    def provide(self, token:type, provider=None, tag:str=None):
        provider = token if provider is None else provider
        if tag is not None:
            token = (token, tag)
        self._registry[token] = provider

    def create(self):
        injector = Injector()
        injector._registry = self._registry.copy()
        return injector

    def get(self, token: T, tag=None) -> T:
        if tag is not None:
            token = (token, tag)
        provider = self._registry.get(token, None)
        if provider is None:
            raise Exception(f'Dependency token={token} not configured')
        if isinstance(provider, LambdaType):
            return provider()
        if not isinstance(provider, type):
            return provider
        if not hasattr(provider, '__init__'):
            return provider()
        if not hasattr(provider.__init__, '__annotations__'):
            return provider()
        args = self.get_dependencies(provider.__init__)
        instance = provider(*args)
        return instance

    def get_dependencies(self, provider):
        dependencies = []
        if not hasattr(provider, '__annotations__'):
            return dependencies
        references = provider.__annotations__.items()
        for name, token in references:
            if name == 'return':
                continue
            dependency = self.get(token)
            dependencies.append(dependency)
        return dependencies