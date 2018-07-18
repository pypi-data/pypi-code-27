# -*- coding: utf-8 -*-

__all__ = ['_utils','functions','main','stats']
dependencies = ['pandas','numpy']
missing_dependencies = []

for dependency in dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError("Missing required dependencies {0}".format(missing_dependencies))
del(dependencies)
del(dependency)
del(missing_dependencies)

from mr_clean.core.api import *
