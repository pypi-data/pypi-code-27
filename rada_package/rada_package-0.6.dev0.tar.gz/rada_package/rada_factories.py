from abc import ABC, abstractmethod

from .rada_databases import UkraineDataBase, PolandDataBase
from .rada_models import (
    UkraineVerkhovnaRada,
    PolandVerkhovnaRada,
    UkraineFraction,
    PolandFraction,
    UkraineDeputat,
    PolandDeputat,
)
from .rada_consoles import UkraineConsole, PolandConsole


class RadaFactory(ABC):

    @abstractmethod
    def __init__(self):
        pass


class UkraineRadaFactory(RadaFactory):

    def __init__(self):
        self.rada_class = UkraineVerkhovnaRada
        self.fraction_class = UkraineFraction
        self.deputat_class = UkraineDeputat
        self.console_class = UkraineConsole
        self.db_class = UkraineDataBase

    def __call__(self, *args, **kwargs):
        rada = self.rada_class()
        return UkraineConsole(rada, self.fraction_class, self.deputat_class, self.db_class)


class PolandRadaFactory(RadaFactory):

    def __init__(self):
        self.rada_class = PolandVerkhovnaRada
        self.fraction_class = PolandFraction
        self.deputat_class = PolandDeputat
        self.console_class = PolandConsole
        self.db_class = PolandDataBase

    def __call__(self, *args, **kwargs):
        rada = self.rada_class()
        return PolandConsole(rada, self.fraction_class, self.deputat_class, self.db_class)