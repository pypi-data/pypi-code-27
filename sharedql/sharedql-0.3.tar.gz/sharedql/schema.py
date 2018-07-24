from __future__ import print_function
import sys
import importlib
from django.conf import settings
import graphene

from .base import sharedql_query, sharedql_mutation

for imports in settings.INSTALLED_APPS:

    imports = imports + ".schema"

    try:
        mod = importlib.import_module(imports)
    except ImportError:
        # print("Failed to load {module}".format(module=imports), file=sys.stderr)
        pass

shared_classes = tuple(sharedql_query.query_classes + [graphene.ObjectType, object])
shared_mutations = tuple(sharedql_mutation.mutation_classes + [graphene.ObjectType, object])

SharedQuery = type('Query', shared_classes, {})
SharedMutation = type('Mutation', shared_mutations, {})

schema = graphene.Schema(query=SharedQuery, mutation=SharedMutation)