"""Package for using json hyper-schema in pyramid applications using cornice
and colander."""
from pyramid.config import Configurator
from .deriver import schema_validated_view

__all__ = ["schema_validated_view"]


def includeme(config: Configurator):
    config.add_view_deriver(schema_validated_view)
