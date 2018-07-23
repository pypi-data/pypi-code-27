from __future__ import print_function
import sys
import importlib
from django.conf import settings
import graphene

from .base import sharedql

for imports in settings.INSTALLED_APPS:

    imports = imports + ".schema"

    try:
        mod = importlib.import_module(imports + ".schema")
    except ImportError:
        pass
        # print("Failed to load {module}".format(module=imports),file=sys.stderr)

bases = tuple(sharedql.query_classes + [graphene.ObjectType, object])

# for cls in bases:
#     print("Including '{}' in global GraphQL Query...".format(cls.__name__))

SharedQuery = type('Query', bases, {})

schema = graphene.Schema(query=SharedQuery)