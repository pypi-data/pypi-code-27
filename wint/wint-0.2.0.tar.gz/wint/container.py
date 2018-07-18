from . import punq


class Container:
    EMPTY = "__EMPTY__"

    def __init__(self):
        self._initialize_container()

    def _initialize_container(self):
        self._container = punq.Container()

    def resolve(self, typ, **kwargs):
        try:
            return self._container.resolve(typ, **kwargs)
        except punq.MissingDependencyException:
            return self.EMPTY

    def register(self, typ, impl=None, **kwargs):
        return self._container.register(typ, impl, **kwargs)


class ContainerProvider:
    INSTANCE: Container = None

    @classmethod
    def get(cls) -> Container:
        if cls.INSTANCE is None:
            cls.set(cls._create_container())

        return cls.INSTANCE

    @classmethod
    def set(cls, container: Container, force=False):
        if cls.INSTANCE is not None and not force:
            raise ValueError("Can not set container, because it is already set.")

        cls.INSTANCE = container

    @classmethod
    def _create_container(cls):
        return Container()

    @classmethod
    def resolve(cls, typ, **kwargs):
        return cls.get().resolve(typ, **kwargs)
